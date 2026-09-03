from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    answers = relationship("Answer", back_populates="session")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    question = Column(Text)
    transcript = Column(Text)
    eye_contact_score = Column(Float)
    posture_score = Column(Float)
    content_score = Column(Float)
    feedback = Column(Text)
    session = relationship("Session", back_populates="answers")