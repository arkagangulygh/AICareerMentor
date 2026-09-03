
from sqlalchemy import Column, Integer, Text, ForeignKey, String
from app.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Groups multiple questions into one interview
    session_id = Column(
        String,
        nullable=False,
        index=True
    )

    # Question number: 1, 2, 3, 4, 5
    question_number = Column(
        Integer,
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=True
    )

    score = Column(
        Integer,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )
