from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def run_script(script_name: str) -> dict:
    script_path = REPO_ROOT / script_name
    if not script_path.exists():
        return {'status': 'error', 'error': f'Script not found: {script_name}'}

    result = subprocess.run(
        ['python', str(script_path)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=300,
        env=os.environ.copy(),
    )
    return {
        'status': 'ok' if result.returncode == 0 else 'error',
        'returncode': result.returncode,
        'stdout': result.stdout[-4000:],
        'stderr': result.stderr[-4000:],
    }
