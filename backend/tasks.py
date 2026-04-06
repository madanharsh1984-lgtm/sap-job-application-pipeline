import os
from datetime import datetime
from celery_app import celery_app
from scrapers import ApifyScraper
from database import SessionLocal
import models
from resume_service import ResumeService

@celery_app.task(name="tasks.run_daily_scrape")
def run_daily_scrape():
    # ... (existing code)
    db = SessionLocal()
    # ... (rest of the scrape logic)
    db.commit()
    db.close()
    return {"status": "complete"}

@celery_app.task(name="tasks.tailor_and_apply")
def tailor_and_apply(user_id: str, lead_id: str, resume_id: str):
    """Asynchronous task to tailor a resume and apply for a job."""
    db = SessionLocal()
    
    # 1. Fetch data from DB
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    lead = db.query(models.JobLead).filter(models.JobLead.lead_id == lead_id).first()
    master_resume = db.query(models.Resume).filter(models.Resume.resume_id == resume_id).first()
    
    if not all([user, lead, master_resume]):
        return {"status": "error", "message": "Required data missing from database."}

    # 2. Update application status in DB
    app_entry = models.Application(
        user_id=user.user_id,
        lead_id=lead.lead_id,
        resume_id=master_resume.resume_id,
        status="Processing",
        log="AI tailoring started..."
    )
    db.add(app_entry)
    db.commit()
    db.refresh(app_entry)

    # 3. Trigger AI Tailoring
    resume_service = ResumeService()
    # For local dev, we assume the resume is on disk at s3_path
    # In prod, we would download from S3 first
    output_dir = "temp_resumes"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        result = resume_service.generate_tailored_resume(
            master_resume.s3_path, 
            lead.raw_text, 
            output_dir
        )
        
        if result:
            app_entry.log = f"Tailoring complete. Match Score: {result['match_score']}%"
            # In a real app, we would now trigger the automation script (LinkedIn/Email)
            # using the tailored file at result['file_path']
            app_entry.status = "Sent" # For MVP, we mark as sent after tailoring
            app_entry.sent_at = datetime.utcnow()
        else:
            app_entry.status = "Failed"
            app_entry.log = "AI tailoring failed to generate a response."
            
    except Exception as e:
        app_entry.status = "Failed"
        app_entry.log = f"Execution Error: {str(e)}"
    
    db.commit()
    db.close()
    return {"status": app_entry.status, "log": app_entry.log}
