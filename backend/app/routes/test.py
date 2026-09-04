
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.models.test import Test
from app.models.resume import Resume
from app.utils.security import get_current_user

from app.services.test_service import (
    generate_test_questions,
    evaluate_test_answer
)


router = APIRouter(
    prefix="/test",
    tags=["Weekly Test"]
)


TOTAL_QUESTIONS = 5


class TestAnswer(BaseModel):
    test_id: int
    answer: str


@router.post("/generate")
def generate_test(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

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

    session_id = str(uuid.uuid4())

    # Generate all 5 questions in ONE Gemini call
    generated_questions = generate_test_questions(
        resume.extracted_text
    )

    questions = []

    for question_data in generated_questions:

        question_number = question_data["question_number"]
        question = question_data["question"]

        test = Test(
            user_id=user_id,
            test_session_id=session_id,
            question_number=question_number,
            question=question
        )

        db.add(test)
        db.commit()
        db.refresh(test)

        questions.append({
            "test_id": test.id,
            "question_number": question_number,
            "question": question
        })

    return {
        "message": "Weekly test generated successfully",
        "session_id": session_id,
        "total_questions": TOTAL_QUESTIONS,
        "questions": questions
    }


@router.post("/submit")
def submit_answer(
    data: TestAnswer,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    test = db.query(Test).filter(
        Test.id == data.test_id,
        Test.user_id == user_id
    ).first()

    if not test:
        raise HTTPException(
            status_code=404,
            detail="Test question not found"
        )

    if test.answer:
        raise HTTPException(
            status_code=400,
            detail="This question has already been answered"
        )

    evaluation = evaluate_test_answer(
        test.question,
        data.answer
    )

    test.answer = data.answer
    test.feedback = evaluation

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

    test.score = score

    db.commit()
    db.refresh(test)

    # Check whether all questions in this test session
    # have been answered
    session_tests = db.query(Test).filter(
        Test.test_session_id == test.test_session_id,
        Test.user_id == user_id
    ).order_by(
        Test.question_number
    ).all()

    answered_tests = [
        item
        for item in session_tests
        if item.score is not None
    ]

    completed = (
        len(answered_tests) == TOTAL_QUESTIONS
    )

    response = {
        "message": "Answer evaluated successfully",
        "test_id": test.id,
        "question_number": test.question_number,
        "score": test.score,
        "feedback": test.feedback,
        "completed": completed
    }

    # If all 5 questions are answered,
    # calculate final result
    if completed:

        total_score = sum(
            item.score
            for item in answered_tests
        )

        average_score = (
            total_score / len(answered_tests)
        )

        response["total_score"] = total_score
        response["average_score"] = round(
            average_score,
            2
        )

    return response


@router.get("/history")
def test_history(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    tests = db.query(Test).filter(
        Test.user_id == user_id
    ).order_by(
        Test.test_session_id,
        Test.question_number
    ).all()

    if not tests:
        return {
            "message": "No test history found"
        }

    sessions = {}

    for test in tests:

        if test.test_session_id not in sessions:

            sessions[test.test_session_id] = []

        sessions[test.test_session_id].append({
            "question_number": test.question_number,
            "test_id": test.id,
            "question": test.question,
            "answer": test.answer,
            "score": test.score,
            "feedback": test.feedback
        })

    results = []

    for session_id, questions in sessions.items():

        answered = [
            q for q in questions
            if q["score"] is not None
        ]

        if answered:

            total_score = sum(
                q["score"]
                for q in answered
            )

            average_score = (
                total_score / len(answered)
            )

        else:

            average_score = 0

        results.append({
            "session_id": session_id,
            "total_questions": TOTAL_QUESTIONS,
            "answered_questions": len(answered),
            "average_score": round(
                average_score,
                2
            ),
            "questions": questions
        })

    return {
        "tests": results
    }
