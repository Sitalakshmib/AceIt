from sqlalchemy.orm import Session
from models.interview_question import InterviewQuestion
import random

def get_next_question(
    db: Session,
    domain: str,
    topic: str,
    difficulty: str,
    exclude_ids: list[int]
):
    """
    Fetch one interview question from DB based on filters.
    """

    query = db.query(InterviewQuestion).filter(
        InterviewQuestion.domain == domain,
        InterviewQuestion.topic == topic,
        InterviewQuestion.difficulty == difficulty
    )

    # Exclude already asked questions
    if exclude_ids:
        query = query.filter(~InterviewQuestion.id.in_(exclude_ids))

    questions = query.all()

    if not questions:
        return None

    return random.choice(questions)
