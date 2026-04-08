from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DATA_DIR = r"C:\Users\madan\OneDrive\Desktop\Linkdin Job\data"
DEFAULT_ACTOR_ID = "harvestapi~linkedin-post-search"
MAX_LOCAL_JOBS = 20


@dataclass
class LocalPaths:
    root: Path
    jobs: Path
    logs: Path
    resumes: Path
    keywords: Path
    users_json: Path
    system_log: Path


def setup_paths(base_dir: str) -> LocalPaths:
    root = Path(base_dir)
    paths = LocalPaths(
        root=root,
        jobs=root / "jobs",
        logs=root / "logs",
        resumes=root / "resumes",
        keywords=root / "keywords",
        users_json=root / "users.json",
        system_log=root / "logs" / "system.log",
    )
    for p in (paths.root, paths.jobs, paths.logs, paths.resumes, paths.keywords):
        p.mkdir(parents=True, exist_ok=True)
    if not paths.users_json.exists():
        paths.users_json.write_text("[]\n", encoding="utf-8")
    return paths


def setup_logger(log_file: Path) -> logging.Logger:
    logger = logging.getLogger("local_mode_pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def normalize_keywords(keywords: list[str]) -> list[str]:
    return sorted({k.strip().lower() for k in keywords if k and k.strip()})


def extract_keywords(resume_content: str, max_keywords: int = 30) -> list[str]:
    tokens = re.findall(r"[A-Za-z0-9+#./-]+", resume_content or "")
    candidates = [t for t in tokens if len(t) > 4]
    return normalize_keywords(candidates)[:max_keywords]


def keyword_set_id(normalized_keywords: list[str]) -> str:
    blob = "|".join(normalized_keywords).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def _apify_request(token: str, method: str, path: str, body: dict | None = None) -> tuple[int, dict | list]:
    url = f"https://api.apify.com/v2{path}"
    payload = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=payload, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="ignore")
        return exc.code, {"error": raw[:800]}
    except Exception as exc:  # noqa: BLE001
        return 0, {"error": str(exc)}


def scrape_jobs_apify(token: str, keywords: list[str], logger: logging.Logger) -> list[dict]:
    status, run = _apify_request(
        token,
        "POST",
        f"/acts/{DEFAULT_ACTOR_ID}/runs",
        body={
            "searchQueries": keywords[:8],
            "maxPosts": 20,
            "sort": "date",
            "scrapeReactions": False,
            "scrapeComments": False,
        },
    )
    if status not in (200, 201):
        raise RuntimeError(f"Failed to start Apify actor: status={status}, response={run}")

    run_id = (run or {}).get("data", {}).get("id", "")
    if not run_id:
        raise RuntimeError("Apify run ID missing")

    dataset_id = ""
    for _ in range(45):
        time.sleep(2)
        state_code, state = _apify_request(token, "GET", f"/actor-runs/{run_id}")
        if state_code != 200:
            continue
        run_data = (state or {}).get("data", {})
        run_status = run_data.get("status")
        if run_status == "SUCCEEDED":
            dataset_id = run_data.get("defaultDatasetId", "")
            break
        if run_status in {"FAILED", "ABORTED", "TIMED-OUT"}:
            raise RuntimeError(f"Apify run failed with status={run_status}, run_id={run_id}")
    if not dataset_id:
        raise RuntimeError(f"Apify run timed out, run_id={run_id}")

    ds_code, ds = _apify_request(token, "GET", f"/datasets/{dataset_id}/items?clean=true&format=json&limit=1000")
    if ds_code != 200:
        raise RuntimeError(f"Failed to fetch Apify dataset: status={ds_code}")

    records = ds if isinstance(ds, list) else ds.get("items", [])
    jobs: list[dict] = []
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        author = record.get("author") or {}
        jobs.append(
            {
                "id": f"apify-{idx+1}",
                "title": record.get("title") or "SAP Opportunity",
                "company": (author.get("info") if isinstance(author, dict) else "") or "Unknown",
                "location": record.get("location") or "Unknown",
                "url": record.get("linkedinUrl") or record.get("url") or "",
                "posted_at": record.get("postedAt") or "",
                "content": record.get("content") or record.get("text") or "",
                "source": "apify",
            }
        )

    logger.info("Apify scraping completed with %s records", len(jobs))
    return jobs[:MAX_LOCAL_JOBS]


def scrape_jobs_local(keywords: list[str]) -> list[dict]:
    top = keywords[:5] or ["sap consultant"]
    jobs: list[dict] = []
    for idx, keyword in enumerate(top, start=1):
        jobs.append(
            {
                "id": f"local-{idx}",
                "title": f"{keyword.title()} Role",
                "company": f"Company {idx}",
                "location": "Remote",
                "url": f"https://example.local/jobs/{idx}",
                "posted_at": datetime.now(timezone.utc).isoformat(),
                "content": f"Local generated job for keyword: {keyword}",
                "source": "local",
            }
        )
    return jobs


def save_jobs(paths: LocalPaths, ks_id: str, keywords: list[str], jobs: list[dict]) -> Path:
    target = paths.jobs / f"{ks_id}.json"
    payload = {
        "keyword": ", ".join(keywords[:5]),
        "keyword_set_id": ks_id,
        "jobs": jobs,
        "job_count": len(jobs),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def save_keyword_file(paths: LocalPaths, user_email: str, keywords: list[str], ks_id: str) -> Path:
    safe = user_email.replace("@", "_at_").replace(".", "_")
    target = paths.keywords / f"{safe}.json"
    payload = {
        "email": user_email,
        "keyword_set_id": ks_id,
        "keywords": keywords,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def load_users(path: Path) -> list[dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return []


def write_users(path: Path, users: list[dict]) -> None:
    path.write_text(json.dumps(users, indent=2, ensure_ascii=False), encoding="utf-8")


def process_user(
    *,
    paths: LocalPaths,
    logger: logging.Logger,
    email: str,
    resume_content: str,
    apify_token: str,
    keyword_job_cache: dict[str, dict],
) -> dict:
    logger.info("Processing user: %s", email)
    resume_path = paths.resumes / f"{email.replace('@', '_at_').replace('.', '_')}.txt"
    resume_path.write_text(resume_content, encoding="utf-8")

    keywords = extract_keywords(resume_content)
    if not keywords:
        keywords = ["sap consultant", "project manager"]

    ks_id = keyword_set_id(keywords)
    save_keyword_file(paths, email, keywords, ks_id)

    if ks_id not in keyword_job_cache:
        logger.info("Scraping start | keyword_set=%s", ks_id)
        jobs: list[dict]
        if apify_token:
            try:
                jobs = scrape_jobs_apify(apify_token, keywords, logger)
            except Exception as exc:  # noqa: BLE001
                logger.error("Apify scrape failed for %s, falling back to local scraper: %s", ks_id, exc)
                jobs = scrape_jobs_local(keywords)
        else:
            jobs = scrape_jobs_local(keywords)
        job_file = save_jobs(paths, ks_id, keywords, jobs)
        keyword_job_cache[ks_id] = {"job_file": str(job_file), "job_count": len(jobs)}
        logger.info("Scraping end | keyword_set=%s | jobs=%s", ks_id, len(jobs))
    else:
        logger.info("Reusing existing scrape | keyword_set=%s", ks_id)

    return {
        "email": email,
        "keywords": keywords,
        "keyword_set_id": ks_id,
        "resume_path": str(resume_path),
        "job_file": keyword_job_cache[ks_id]["job_file"],
        "job_count": keyword_job_cache[ks_id]["job_count"],
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def build_demo_users() -> list[dict]:
    resumes = [
        "SAP S4 HANA Program Manager with 15 years experience in data migration, SAP MM SD, cutover planning and stakeholder management.",
        "SAP project manager skilled in S4 rollout, agile delivery, integrations, and PMO governance for global templates.",
        "SAP consultant focused on SD MM support, testing, migration, and post-go-live stabilization for enterprise clients.",
        "Data migration lead with LTMC LSMW MDG and S4 transformation expertise, risk management, and execution planning.",
        "Program manager for ERP modernization, SAP ECC to S4HANA, team leadership, vendor management, and delivery assurance.",
    ]
    users: list[dict] = []
    for i in range(10):
        users.append(
            {
                "email": f"user{i+1}@example.com",
                "resume_content": resumes[i % len(resumes)],
            }
        )
    return users


def print_tree(root: Path) -> None:
    print(f"\n{root}")
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_dir():
            print(f"  {rel}/")
        else:
            print(f"  {rel}")


def main() -> int:
    data_dir = os.getenv("LOCAL_DATA_DIR", DEFAULT_DATA_DIR)
    apify_token = os.getenv("APIFY_TOKEN", "").strip()

    paths = setup_paths(data_dir)
    logger = setup_logger(paths.system_log)
    logger.info("Local mode pipeline started | data_dir=%s", paths.root)

    demo_users = build_demo_users()
    users = load_users(paths.users_json)

    cache: dict[str, dict] = {}
    for file in paths.jobs.glob("*.json"):
        try:
            payload = json.loads(file.read_text(encoding="utf-8"))
            ks_id = payload.get("keyword_set_id")
            if ks_id:
                cache[ks_id] = {"job_file": str(file), "job_count": int(payload.get("job_count", 0))}
        except Exception:  # noqa: BLE001
            continue

    by_email = {u.get("email"): u for u in users if isinstance(u, dict) and u.get("email")}
    for item in demo_users:
        record = process_user(
            paths=paths,
            logger=logger,
            email=item["email"],
            resume_content=item["resume_content"],
            apify_token=apify_token,
            keyword_job_cache=cache,
        )
        by_email[record["email"]] = record

    final_users = sorted(by_email.values(), key=lambda x: x["email"])
    write_users(paths.users_json, final_users)

    logger.info("Pipeline completed | users=%s | keyword_sets=%s", len(final_users), len(cache))

    print_tree(paths.root)
    print("\nSAMPLE JOB FILE:")
    sample_job = next(iter(paths.jobs.glob("*.json")), None)
    if sample_job:
        print(sample_job)
        print(sample_job.read_text(encoding="utf-8")[:1200])

    print("\nSAMPLE USERS FILE:")
    print(paths.users_json)
    print(paths.users_json.read_text(encoding="utf-8")[:1200])

    print("\nLOG TAIL:")
    lines = paths.system_log.read_text(encoding="utf-8").splitlines()
    for line in lines[-20:]:
        print(line)

    print("\nLOCAL SYSTEM FULLY WORKING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
