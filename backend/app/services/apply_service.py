from app.services.script_runner import run_script


def trigger_linkedin_apply() -> dict:
    return run_script('linkedin_easy_apply.py')
