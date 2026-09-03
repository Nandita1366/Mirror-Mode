from pydantic import BaseModel
from typing import Optional

class StartSessionRequest(BaseModel):
    role: str

class StartSessionResponse(BaseModel):
    session_id: int
    question: str

class SubmitAnswerRequest(BaseModel):
    session_id: int
    question: str
    transcript: str

class SubmitAnswerResponse(BaseModel):
    content_score: int
    structure_score: int
    strength: str
    improvement: str
    next_question: Optional[str] = None

class SessionReportResponse(BaseModel):
    session_id: int
    total_questions: int
    average_content_score: float
    report: str