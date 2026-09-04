
import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_test_questions(resume_text):

    prompt = f"""
You are an AI career assessment system.

Candidate Resume:
{resume_text}

Generate exactly 5 technical questions for a weekly
career assessment test.

Difficulty progression:

Question 1: Easy
Question 2: Easy/Moderate
Question 3: Moderate
Question 4: Moderate/Advanced
Question 5: Advanced

Rules:

1. Base the questions on technologies, skills,
   projects or concepts mentioned in the resume.
2. Test technical understanding.
3. Each question must contain exactly ONE question.
4. Do not provide answers.
5. Keep questions clear and concise.
6. Avoid unrelated topics.
7. Increase difficulty according to the question number.
8. Return ONLY valid JSON.
9. Do not include markdown or ```json.

Return exactly this format:

[
    {{
        "question_number": 1,
        "question": "..."
    }},
    {{
        "question_number": 2,
        "question": "..."
    }},
    {{
        "question_number": 3,
        "question": "..."
    }},
    {{
        "question_number": 4,
        "question": "..."
    }},
    {{
        "question_number": 5,
        "question": "..."
    }}
]
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    response_text = interaction.output_text.strip()

    questions = json.loads(response_text)

    if not isinstance(questions, list) or len(questions) != 5:
        raise ValueError(
            "Gemini did not return exactly 5 questions"
        )

    return questions


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
