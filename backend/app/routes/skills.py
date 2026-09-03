
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job import Job
from app.models.resume import Resume
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/skills",
    tags=["Skill Gap"]
)


@router.post("/analyze")
def analyze_skill_gap(
    job_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # Find the job belonging to the logged-in user
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Find the latest resume of the logged-in user
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

    # Get required skills from the job
    required_skills = []

    if job.required_skills:
        required_skills = [
            skill.strip()
            for skill in job.required_skills.split(",")
        ]

    # Resume text
    resume_text = resume.extracted_text.lower()

    matched_skills = []
    missing_skills = []

    # Compare job skills with resume
    for skill in required_skills:

        if skill.lower() in resume_text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Assign priority
    skill_gap = []

    for skill in missing_skills:

        if skill.lower() in [
            "python",
            "java",
            "javascript",
            "sql",
            "postgresql"
        ]:
            priority = "high"

        elif skill.lower() in [
            "fastapi",
            "django",
            "docker",
            "aws",
            "react"
        ]:
            priority = "medium"

        else:
            priority = "low"

        skill_gap.append({
            "skill": skill,
            "priority": priority
        })

    return {
        "job_id": job.id,
        "job_title": job.title,
        "resume_id": resume.id,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_gap": skill_gap
    }
