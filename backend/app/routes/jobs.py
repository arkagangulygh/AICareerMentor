
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate
from app.utils.security import get_current_user

from app.models.resume import Resume
router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# Skills our system can recognize
SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "fastapi",
    "django",
    "flask",
    "spring boot",
    "react",
    "node.js",
    "express",
    "html",
    "css",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch"
]


def extract_skills(description):

    description_lower = description.lower()

    skills_found = []

    for skill in SKILLS:

        if skill.lower() in description_lower:
            skills_found.append(skill)

    return skills_found


@router.post("/analyze")
def analyze_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # Extract skills from job description
    skills = extract_skills(
        job_data.description
    )

    # Convert skills list into text for database
    required_skills = ", ".join(skills)

    # Create job
    new_job = Job(
        user_id=user_id,
        title=job_data.title,
        description=job_data.description,
        required_skills=required_skills
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job description analyzed successfully",
        "job_id": new_job.id,
        "title": new_job.title,
        "required_skills": skills
    }


@router.post("/match")
def match_job(
    job_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # Get the job
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Get user's resume
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

    # Convert resume text to lowercase
    resume_text = resume.extracted_text.lower()

    # Get required skills from job
    required_skills = []

    if job.required_skills:
        required_skills = [
            skill.strip()
            for skill in job.required_skills.split(",")
        ]

    matched_skills = []
    missing_skills = []

    # Compare skills
    for skill in required_skills:

        if skill.lower() in resume_text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Calculate match percentage
    if len(required_skills) > 0:
        match_percentage = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        match_percentage = 0

    return {
        "job_id": job.id,
        "job_title": job.title,
        "resume_id": resume.id,
        "match_percentage": round(match_percentage, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
