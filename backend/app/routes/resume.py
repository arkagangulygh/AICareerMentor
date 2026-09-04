
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pypdf import PdfReader
import os

from app.database import get_db
from app.models.resume import Resume
from app.services.resume_services import calc_resume_score
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


UPLOAD_DIR = "uploads/resumes"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # Check file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Save PDF
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    # Extract text
    reader = PdfReader(file_path)

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text += text + "\n"

    # Save resume information in database
    resume = Resume(
        user_id=user_id,
        filename=file.filename,
        file_path=file_path,
        extracted_text=extracted_text
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "filename": file.filename,
        "text_length": len(extracted_text)
    }


@router.get("/score/{resume_id}")
def get_resume_score(
    resume_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    # Find resume belonging to logged-in user
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == user_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # Calculate score
    result = calc_resume_score(
        resume.extracted_text
    )

    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        **result
    }

