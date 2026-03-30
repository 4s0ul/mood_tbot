from datetime import datetime

from pydantic import BaseModel


class MoodResult(BaseModel):
    tg_id: int
    username: str
    name: str
    date: datetime
    day_number: int
    mood_score: float
    emotions: str  # ????
    daily_question: str
    daily_answer: str
    comment: str
    submitted_at: datetime
