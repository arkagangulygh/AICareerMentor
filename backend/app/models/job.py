from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=True)

    description = Column(Text, nullable=False)

    required_skills = Column(Text, nullable=True)