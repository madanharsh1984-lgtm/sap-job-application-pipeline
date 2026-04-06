from database import SessionLocal
import models

def clean_db():
    db = SessionLocal()
    # Delete all users starting with 'test_'
    test_users = db.query(models.User).filter(models.User.email.like('test_%')).all()
    for user in test_users:
        db.delete(user)
        print(f"Deleted test user: {user.email}")
    
    # Delete the user's accounts to be safe
    user_emails = ["myinvestment234@gmail.com", "myinvestments234@gmail.com", "test_whatsapp_log2@gmail.com", "test_whatsapp_mock@gmail.com"]
    for email in user_emails:
        u = db.query(models.User).filter(models.User.email == email).first()
        if u:
            db.delete(u)
            print(f"Deleted user account: {email}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    clean_db()
