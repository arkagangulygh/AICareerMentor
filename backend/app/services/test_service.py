
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_test_question(
    resume_text,
    question_number
):

    prompt = f"""
You are an AI career assessment system.

Candidate Resume:
{resume_text}

Generate ONE technical question for a weekly
career assessment test.

This is question {question_number} of 5.

Difficulty progression:

Question 1: Easy
Question 2: Easy/Moderate
Question 3: Moderate
Question 4: Moderate/Advanced
Question 5: Advanced

Rules:

1. Base the question on technologies, skills,
   projects or concepts mentioned in the resume.
2. The question should test technical understanding.
3. Ask exactly ONE question.
4. Do not provide the answer.
5. Keep the question clear and concise.
6. Avoid unrelated topics.
7. Increase difficulty according to the question number.

Return ONLY the question.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text.strip()


def evaluate_test_answer(
    question,
    answer
):

    prompt = f"""
You are an expert technical evaluator.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return exactly:

Score: X/10
Feedback: <short useful feedback>

Rules:
- Score from 0 to 10.
- Judge technical correctness.
- Judge relevance to the question.
- Judge clarity.
- Be fair and constructive.
- Do not give a very long response.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text.strip()
