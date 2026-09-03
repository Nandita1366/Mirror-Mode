import json
from app.llm.groq_client import ask_groq
from app.llm.prompts import QUESTION_GEN_PROMPT, EVAL_PROMPT, REPORT_PROMPT

def generate_question(role: str) -> str:
    prompt = QUESTION_GEN_PROMPT.format(role=role)
    return ask_groq(prompt)

def evaluate_answer(question: str, transcript: str) -> dict:
    prompt = EVAL_PROMPT.format(question=question, transcript=transcript)
    raw = ask_groq(prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"content_score": 0, "structure_score": 0, "strength": "N/A", "improvement": "Could not parse evaluation"}

def generate_report(answers_summary: str) -> str:
    prompt = REPORT_PROMPT.format(answers_summary=answers_summary)
    return ask_groq(prompt)