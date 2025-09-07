from datetime import datetime
from typing import Optional
import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite database URL
DATABASE_URL = "sqlite:///./careq.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)  # Changed from telegram_id to user_id
    name = Column(String, index=True)
    age = Column(Integer)
    symptoms = Column(String) # Stored as JSON string
    triage_score = Column(Integer)
    severity_level = Column(String)
    eta = Column(Integer) # Estimated Time of Arrival in minutes
    queued_at = Column(DateTime, default=datetime.now)
    called = Column(Boolean, default=False)
    lang_code = Column(String, default="en") # New column to store preferred language

    def __repr__(self):
        return f"<Patient(id={self.id}, name='{self.name}', severity='{self.severity_level}')>"

# Create database tables
def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_dynamic_eta(severity_level: str, current_queue_length: int) -> int:
    """
    Calculates dynamic ETA based on severity and current queue.
    This is a simplified model and can be expanded.
    """
    base_wait_time = 10 # minutes per patient if queue is empty for a stable patient

    if severity_level == "Critical":
        return max(5, current_queue_length * 3) # Critical patients get faster estimates
    elif severity_level == "Urgent":
        return max(15, current_queue_length * 7)
    else: # Stable
        return max(30, current_queue_length * 12)
