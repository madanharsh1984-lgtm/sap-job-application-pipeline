from app.services.script_runner import run_script


def trigger_emails() -> dict:
    return run_script('send_sap_emails.py')
