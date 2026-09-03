QUESTION_GEN_PROMPT = """You are a technical interviewer for a {role} position.
Ask one clear, focused interview question. Do not include any preamble or explanation — output only the question."""

EVAL_PROMPT = """You are evaluating a candidate's interview answer.

Question: {question}
Candidate's answer (transcribed): {transcript}

Evaluate on:
1. Content relevance and correctness (1-10)
2. Structure and clarity (1-10)
3. One specific strength
4. One specific improvement

Respond in this exact JSON format:
{{"content_score": <int>, "structure_score": <int>, "strength": "<text>", "improvement": "<text>"}}"""

REPORT_PROMPT = """Given these interview answers and their scores: {answers_summary}

Write a concise overall interview performance report covering:
- Overall readiness assessment
- Top 2 strengths
- Top 2 areas to improve
- One actionable tip for next practice session"""