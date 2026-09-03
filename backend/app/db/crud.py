from sqlalchemy.orm import Session as DBSession
from app.models.db_models import Session, Answer

def create_session(db: DBSession, role: str) -> Session:
    session = Session(role=role)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def save_answer(db: DBSession, session_id: int, question: str, transcript: str, content_score: float, structure_score: float, feedback: str) -> Answer:
    answer = Answer(
        session_id=session_id,
        question=question,
        transcript=transcript,
        content_score=content_score,
        feedback=feedback
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer

def get_session_answers(db: DBSession, session_id: int):
    return db.query(Answer).filter(Answer.session_id == session_id).all()

def get_session(db: DBSession, session_id: int) -> Session:
    return db.query(Session).filter(Session.id == session_id).first()