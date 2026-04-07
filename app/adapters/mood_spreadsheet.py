from loguru import logger

from app.core import GoogleSpreadsheet
from app.models import MoodResult


class MoodSpreadsheet:  # TODO: make this stuff as a separate worker
    def __init__(self, gs_manager: GoogleSpreadsheet) -> None:
        self.gs_manager = gs_manager

    async def write_mood_result(
        self, mood_result: MoodResult, worksheet_ix: int = 0
    ) -> None:
        try:
            await self.gs_manager.append_row(
                values=list(mood_result.model_dump(mode="json").values()),
                worksheet_ix=worksheet_ix,
            )
        except Exception:
            logger.exception("MoodSpreadsheet: failed to write result: {mood_result}")
