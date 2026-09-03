
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_interview_question(
    resume_text,
    job_title,
    job_description,
    question_number=1
):

    prompt = f"""
You are an AI technical interviewer.

You are interviewing a candidate for this job:

Job Title:
{job_title}

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Generate ONE technical interview question.

IMPORTANT INTERVIEW RULES:

1. Start with an easy or moderate question.
2. The question must be something the candidate can reasonably answer
   based on their resume, projects, skills, or the job description.
3. Prefer questions about technologies and projects explicitly mentioned
   in the candidate's resume.
4. Do NOT immediately ask advanced system-design questions.
5. Do NOT combine multiple questions into one.
6. Ask exactly ONE question.
7. Do not provide the answer.
8. Keep the question clear and concise.
9. Avoid questions unrelated to the candidate's resume or the job.
10. The question should test actual technical understanding, not memorization.

Difficulty progression:

For the first interview question, prefer:
- Basic concepts
- Technologies used in the candidate's projects
- Simple project-related questions

This is question number {question_number} of a 5-question interview.

Difficulty progression:
Question 1: Easy
Question 2: Easy/Moderate
Question 3: Moderate
Question 4: Moderate/Advanced
Question 5: Advanced

Adjust the difficulty according to the question number.

Examples:

If the resume mentions JWT:
"How does JWT-based authentication work, and how did you use it in your project?"

If the resume mentions FastAPI:
"Why did you choose FastAPI for your backend project?"

If the resume mentions MongoDB:
"How did you structure your MongoDB database for your project?"

If the resume mentions a URL shortener:
"Can you explain how your URL shortening service works from the moment a user creates a short URL until someone accesses it?"

Only ask advanced questions such as scalability, distributed systems,
database optimization, or system design after easier questions have been asked.

Return ONLY the interview question.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text.strip()


def evaluate_interview_answer(
    question,
    answer
):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer to the interview question below.

Question:
{question}

Candidate Answer:
{answer}

Give your evaluation in exactly this format:

Score: X/10
Feedback: <short useful feedback>
Strengths: <what the candidate did well>
Weaknesses: <what could be improved>

Rules:
- Score from 0 to 10.
- Judge technical correctness, relevance and clarity.
- Be fair and constructive.
- Do not give an extremely long response.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text.strip()
