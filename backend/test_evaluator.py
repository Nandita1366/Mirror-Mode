from app.llm.evaluator import generate_question, evaluate_answer

q = generate_question("Backend Developer")
print("Question:", q)

result = evaluate_answer(q, "I would use a REST API with proper error handling and status codes.")
print("Evaluation:", result)