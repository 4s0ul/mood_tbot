from app.core import GoogleSheets
from app.models import MoodResult


class MoodSpreadsheet:
    def __init__(self, gs_manager: GoogleSheets) -> None:
        self.gs_manager = gs_manager

    def write_mood_result(self, mood_result: MoodResult, worksheet_ix: int = 0) -> None:
        self.gs_manager.append_row(
            values=list(mood_result.model_dump().values()), worksheet_ix=worksheet_ix
        )
