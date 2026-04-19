from datetime import datetime, timedelta, timezone

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
from sqlmodel import Field, SQLModel


class MoodResult(SQLModel, table=True):
    __tablename__ = "mood_results"

    id: int | None = Field(default=None, primary_key=True)

    tg_id: int | None = Field(default=None, index=True)
    username: str | None = None
    fullname: str | None = None

    mood_score: int | None = None
    energy_level: str | None = None

    # SQLite has JSON support through SQLAlchemy's JSON type.
    emotions: list[str] | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )

    mood_factor: str | None = None
    day_change_wish: str | None = None

    submitted_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone(timedelta(hours=3)))
    )
