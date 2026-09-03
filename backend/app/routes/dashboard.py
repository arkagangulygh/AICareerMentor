
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.resume import Resume
from app.models.job import Job
from app.models.interview import Interview
from app.models.test import Test
from app.utils.security import get_current_user

from app.services.resume_services import calc_resume_score


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # -------------------------
    # Latest Resume
    # -------------------------

    resume = db.query(Resume).filter(
        Resume.user_id == user_id
    ).order_by(
        Resume.id.desc()
    ).first()

    resume_data = None

    if resume:

        resume_result = calc_resume_score(
            resume.extracted_text
        )

        resume_data = {
            "resume_id": resume.id,
            "filename": resume.filename,
            "score": resume_result["score"],
            "skills_found": resume_result["skills_found"],
            "suggestions": resume_result["suggestions"]
        }


    # -------------------------
    # Latest Job
    # -------------------------

    job = db.query(Job).filter(
        Job.user_id == user_id
    ).order_by(
        Job.id.desc()
    ).first()

    job_data = None

    if job:

        required_skills = []

        if job.required_skills:

            required_skills = [
                skill.strip()
                for skill in job.required_skills.split(",")
            ]

        matched_skills = []
        missing_skills = []

        if resume:

            resume_text = resume.extracted_text.lower()

            for skill in required_skills:

                if skill.lower() in resume_text:
                    matched_skills.append(skill)

                else:
                    missing_skills.append(skill)

        match_percentage = 0

        if required_skills:

            match_percentage = (
                len(matched_skills) /
                len(required_skills)
            ) * 100

        job_data = {
            "job_id": job.id,
            "title": job.title,
            "required_skills": required_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percentage": round(
                match_percentage,
                2
            )
        }


    # -------------------------
    # Latest Interview
    # -------------------------

    interview = db.query(Interview).filter(
        Interview.user_id == user_id,
        Interview.score.isnot(None)
    ).order_by(
        Interview.id.desc()
    ).first()

    interview_data = None

    if interview:

        interview_session = db.query(
            Interview
        ).filter(
            Interview.user_id == user_id,
            Interview.session_id == interview.session_id,
            Interview.score.isnot(None)
        ).all()

        total_score = sum(
            item.score
            for item in interview_session
        )

        average_score = (
            total_score /
            len(interview_session)
        )

        interview_data = {
            "session_id": interview.session_id,
            "answered_questions": len(
                interview_session
            ),
            "average_score": round(
                average_score,
                2
            )
        }


    # -------------------------
    # Latest Weekly Test
    # -------------------------

    test = db.query(Test).filter(
        Test.user_id == user_id,
        Test.score.isnot(None)
    ).order_by(
        Test.id.desc()
    ).first()

    test_data = None

    if test:

        test_session = db.query(Test).filter(
            Test.user_id == user_id,
            Test.test_session_id == test.test_session_id,
            Test.score.isnot(None)
        ).all()

        total_score = sum(
            item.score
            for item in test_session
        )

        average_score = (
            total_score /
            len(test_session)
        )

        test_data = {
            "session_id": test.test_session_id,
            "answered_questions": len(
                test_session
            ),
            "average_score": round(
                average_score,
                2
            )
        }


    # -------------------------
    # Dashboard Response
    # -------------------------

    return {
        "user_id": user_id,

        "resume": resume_data,

        "latest_job": job_data,

        "latest_interview": interview_data,

        "latest_weekly_test": test_data
    }
