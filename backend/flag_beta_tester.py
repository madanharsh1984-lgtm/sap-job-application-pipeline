import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

# Database configuration (matching database.py or using env)
DATABASE_URL = "postgresql://postgres:password@localhost:5432/sap_saas"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def flag_beta_tester(email):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            user.is_beta_tester = True
            user.subscription_tier = "Pro" # Granting Pro for beta testing
            db.commit()
            print(f"Successfully flagged {email} as a Beta Tester and granted Pro access.")
        else:
            print(f"User with email {email} not found.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    flag_beta_tester("myinvestments234@gmail.com")
