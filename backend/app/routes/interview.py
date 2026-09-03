
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.models.interview import Interview
from app.models.job import Job
from app.models.resume import Resume
from app.utils.security import get_current_user

from app.services.interview_services import (
    generate_interview_question,
    evaluate_interview_answer
)


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


TOTAL_QUESTIONS = 5


class InterviewAnswer(BaseModel):
    interview_id: int
    answer: str


# --------------------------------------------------
# START INTERVIEW
# --------------------------------------------------

@router.post("/start")
def start_interview(
    job_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # Find job belonging to logged-in user
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Find latest resume
    resume = db.query(Resume).filter(
        Resume.user_id == user_id
    ).order_by(
        Resume.id.desc()
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # Create unique interview session
    session_id = str(uuid.uuid4())

    # Generate Question 1
    question = generate_interview_question(
        resume.extracted_text,
        job.title,
        job.description,
        1
    )

    interview = Interview(
        user_id=user_id,
        session_id=session_id,
        question_number=1,
        question=question
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return {
        "message": "Interview started successfully",
        "session_id": session_id,
        "interview_id": interview.id,
        "question_number": 1,
        "total_questions": TOTAL_QUESTIONS,
        "job_id": job.id,
        "job_title": job.title,
        "question": question
    }


# --------------------------------------------------
# ANSWER INTERVIEW QUESTION
# --------------------------------------------------

@router.post("/answer")
def answer_interview(
    data: InterviewAnswer,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # Find interview question belonging to logged-in user
    interview = db.query(Interview).filter(
        Interview.id == data.interview_id,
        Interview.user_id == user_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview question not found"
        )

    # Prevent answering the same question twice
    if interview.answer:
        raise HTTPException(
            status_code=400,
            detail="This question has already been answered"
        )

    # Evaluate answer using Gemini
    evaluation = evaluate_interview_answer(
        interview.question,
        data.answer
    )

    # Save answer
    interview.answer = data.answer

    # Save complete AI feedback
    interview.feedback = evaluation

    # Extract score from Gemini response
    score = None

    for line in evaluation.split("\n"):

        if line.strip().startswith("Score:"):

            try:
                score_text = line.split("/")[0]

                score = int(
                    score_text.replace(
                        "Score:",
                        ""
                    ).strip()
                )

            except ValueError:
                score = None

            break

    interview.score = score

    db.commit()
    db.refresh(interview)

    # --------------------------------------------------
    # CHECK IF INTERVIEW IS COMPLETE
    # --------------------------------------------------

    if interview.question_number >= TOTAL_QUESTIONS:

        return {
            "message": "Interview completed",
            "session_id": interview.session_id,
            "interview_id": interview.id,
            "question_number": interview.question_number,
            "score": interview.score,
            "feedback": interview.feedback,
            "next_question": False
        }

    # --------------------------------------------------
    # GENERATE NEXT QUESTION
    # --------------------------------------------------

    # Find latest resume
    resume = db.query(Resume).filter(
        Resume.user_id == user_id
    ).order_by(
        Resume.id.desc()
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # Find the job associated with this interview session.
    # Since the current Interview model does not store job_id,
    # use the user's latest job for now.
    job = db.query(Job).filter(
        Job.user_id == user_id
    ).order_by(
        Job.id.desc()
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Calculate next question number
    next_question_number = (
        interview.question_number + 1
    )

    # Generate next question with correct difficulty
    next_question = generate_interview_question(
        resume.extracted_text,
        job.title,
        job.description,
        next_question_number
    )

    # Save next question
    next_interview = Interview(
        user_id=user_id,
        session_id=interview.session_id,
        question_number=next_question_number,
        question=next_question
    )

    db.add(next_interview)
    db.commit()
    db.refresh(next_interview)

    return {
        "message": "Answer evaluated successfully",
        "session_id": interview.session_id,

        "completed_question": {
            "interview_id": interview.id,
            "question_number": interview.question_number,
            "score": interview.score,
            "feedback": interview.feedback
        },

        "next_question": {
            "interview_id": next_interview.id,
            "question_number": next_interview.question_number,
            "total_questions": TOTAL_QUESTIONS,
            "question": next_question
        }
    }


# --------------------------------------------------
# INTERVIEW RESULT
# --------------------------------------------------

@router.get("/result")
def get_interview_result(
    session_id: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    interviews = db.query(Interview).filter(
        Interview.session_id == session_id,
        Interview.user_id == user_id
    ).order_by(
        Interview.question_number.asc()
    ).all()

    if not interviews:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    # Only include answered questions
    answered_interviews = [
        interview
        for interview in interviews
        if interview.score is not None
    ]

    if not answered_interviews:
        return {
            "session_id": session_id,
            "message": "No questions have been answered yet"
        }

    # Calculate total score
    total_score = sum(
        interview.score
        for interview in answered_interviews
    )

    # Calculate average score
    average_score = (
        total_score / len(answered_interviews)
    )

    questions = []

    for interview in interviews:

        questions.append({
            "question_number": interview.question_number,
            "interview_id": interview.id,
            "question": interview.question,
            "answer": interview.answer,
            "score": interview.score,
            "feedback": interview.feedback
        })

    return {
        "session_id": session_id,
        "total_questions": TOTAL_QUESTIONS,
        "answered_questions": len(answered_interviews),
        "average_score": round(average_score, 2),
        "questions": questions
    }
