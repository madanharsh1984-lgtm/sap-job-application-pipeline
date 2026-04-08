import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from worker.celery_app import celery_app
from worker.config import settings

logger = logging.getLogger(__name__)


@celery_app.task
def send_application_email(
    user_id: int,
    job_id: int,
    to_email: str,
    subject: str,
    body: str,
) -> dict:
    """Send a job application email.

    If SMTP is not configured, the email is logged instead of sent.

    Args:
        user_id: The ID of the user sending the application.
        job_id: The ID of the job being applied to.
        to_email: Recipient email address.
        subject: Email subject line.
        body: Email body content.

    Returns:
        Dictionary with send status and details.
    """
    logger.info(
        "Sending application email for user_id=%d, job_id=%d to %s",
        user_id,
        job_id,
        to_email,
    )

    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.warning(
            "SMTP not configured — email mock-sent for user_id=%d, job_id=%d "
            "to=%s subject='%s'",
            user_id,
            job_id,
            to_email,
            subject,
        )
        return {
            "status": "mock_sent",
            "to": to_email,
            "subject": subject,
        }

    try:
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(
            "Application email sent successfully for user_id=%d, job_id=%d",
            user_id,
            job_id,
        )
        return {"status": "sent", "to": to_email, "subject": subject}

    except smtplib.SMTPException:
        logger.exception(
            "SMTP error sending email for user_id=%d, job_id=%d",
            user_id,
            job_id,
        )
        return {"status": "error", "to": to_email, "subject": subject}

    except Exception:
        logger.exception(
            "Unexpected error sending email for user_id=%d, job_id=%d",
            user_id,
            job_id,
        )
        return {"status": "error", "to": to_email, "subject": subject}


@celery_app.task
def send_notification(user_id: int, message: str) -> dict:
    """Send a notification email to a user.

    This is a mock implementation that logs the notification. In production,
    the user's email would be fetched from the database and a real email sent.

    Args:
        user_id: The ID of the user to notify.
        message: The notification message content.

    Returns:
        Dictionary with notification status.
    """
    logger.info(
        "Sending notification to user_id=%d: %s",
        user_id,
        message,
    )

    # In production: fetch user email from the backend API and send via SMTP.
    logger.info(
        "Notification mock-sent to user_id=%d: '%s'",
        user_id,
        message[:100],
    )

    return {"status": "mock_sent", "user_id": user_id}
