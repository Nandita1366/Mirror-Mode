from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.db.database import get_db
from app.models.schemas import StartSessionRequest, StartSessionResponse, SubmitAnswerRequest, SubmitAnswerResponse
from app.llm.evaluator import generate_question, evaluate_answer
from app.db.crud import create_session, save_answer
from app.models.schemas import (
    StartSessionRequest, StartSessionResponse,
    SubmitAnswerRequest, SubmitAnswerResponse,
    SessionReportResponse
)
from app.llm.evaluator import generate_question, evaluate_answer, generate_report
from app.db.crud import create_session, save_answer, get_session_answers, get_session
from fastapi import HTTPException
from app.models.schemas import NextQuestionRequest, NextQuestionResponse

router = APIRouter(prefix="/session", tags=["session"])

@router.post("/start", response_model=StartSessionResponse)
def start_session(req: StartSessionRequest, db: DBSession = Depends(get_db)):
    session = create_session(db, req.role)
    question = generate_question(req.role)
    return StartSessionResponse(session_id=session.id, question=question)

@router.post("/answer", response_model=SubmitAnswerResponse)
def submit_answer(req: SubmitAnswerRequest, db: DBSession = Depends(get_db)):
    result = evaluate_answer(req.question, req.transcript)
    save_answer(
        db, req.session_id, req.question, req.transcript,
        result["content_score"], result["structure_score"], result["improvement"]
    )
    return SubmitAnswerResponse(**result)

@router.get("/{session_id}/report", response_model=SessionReportResponse)
def get_report(session_id: int, db: DBSession = Depends(get_db)):
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    answers = get_session_answers(db, session_id)
    if not answers:
        raise HTTPException(status_code=400, detail="No answers submitted yet for this session")

    summary_lines = []
    total_score = 0
    for i, ans in enumerate(answers, start=1):
        summary_lines.append(
            f"Q{i}: {ans.question}\nAnswer: {ans.transcript}\nContent Score: {ans.content_score}/10\nFeedback: {ans.feedback}"
        )
        total_score += ans.content_score

    answers_summary = "\n\n".join(summary_lines)
    avg_score = total_score / len(answers)

    report_text = generate_report(answers_summary)

    return SessionReportResponse(
        session_id=session_id,
        total_questions=len(answers),
        average_content_score=round(avg_score, 2),
        report=report_text
    )

@router.post("/next-question", response_model=NextQuestionResponse)
def next_question(req: NextQuestionRequest):
    question = generate_question(req.role)
    return NextQuestionResponse(question=question)