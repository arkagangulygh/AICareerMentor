from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine,Base

from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.routes.auth import router as auth_router
from app.routes.resume import router as resume_router
from app.routes.jobs import router as jobs_router
from app.routes.skills import router as skills_router
from app.routes.interview import router as interview_router
from app.models.interview import Interview
from app.models.test import Test
from app.routes.test import router as test_router
from app.routes.dashboard import router as dashboard_router
from fastapi import Depends
from app.utils.security import get_current_user
app = FastAPI(
    title="AI Personal Career Mentor",
    description="AI-powered career guidance platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(skills_router)
app.include_router(interview_router)
app.include_router(test_router)
app.include_router(dashboard_router)
@app.get("/")
def home():
    return {
        "message": "AI Personal Career Mentor API is running"
    }

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@app.get("/test-auth")
def test_auth(
    user_id: int = Depends(get_current_user)
):
    return {
        "message": "Authentication successful",
        "user_id": user_id
    }