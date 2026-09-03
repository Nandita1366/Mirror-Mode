from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import session
from app.routers import interview

app = FastAPI(title="MirrorMode API")

app.include_router(session.router)
app.include_router(interview.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "MirrorMode backend is running"}


from app.db.database import engine, Base
from app.models import db_models

Base.metadata.create_all(bind=engine)