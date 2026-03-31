from collections.abc import Sequence
from pathlib import Path

import gspread
from gspread import Worksheet
from loguru import logger


class WorksheetsCache:
    def __init__(self) -> None:
        self._worksheets = {}

    def add_worksheet(self, worksheet_ix: int, worksheet: Worksheet) -> Worksheet:
        if worksheet_ix in self._worksheets:
            return self._worksheets[worksheet_ix]
        self._worksheets[worksheet_ix] = worksheet
        return self._worksheets[worksheet_ix]

    def get_worksheet(self, worksheet_ix: int) -> Worksheet | None:
        if worksheet_ix not in self._worksheets:
            return None
        return self._worksheets[worksheet_ix]


class GoogleSpreadsheet:
    def __init__(self, creds_path: Path, g_spread_key: str) -> None:
        try:
            self.gc = gspread.service_account(filename=creds_path)
        except Exception:
            logger.exception("GoogleSpreadsheet: failed to autorize")
            raise
        try:
            self.spread = self.gc.open_by_key(g_spread_key)
        except Exception:
            logger.exception("GoogleSpreadsheet: spreadsheets key is wrong")
            raise
        self._worksheets: WorksheetsCache | None = None

    def close_spreadsheet(self):
        self.spread.client.session.close()

    def _get_worksheet(self, worksheet_ix) -> Worksheet:
        if not self._worksheets:
            self._worksheets = WorksheetsCache()
        worksheet = self._worksheets.get_worksheet(worksheet_ix)
        if not worksheet:
            try:
                worksheet = self.spread.get_worksheet(worksheet_ix)
            except Exception:
                logger.exception(
                    f"GoogleSpreadsheet: no worksheet with index: {worksheet_ix}"
                )
                raise
            self._worksheets.add_worksheet(worksheet_ix, worksheet)
        return worksheet

    def append_row(self, values: Sequence, worksheet_ix: int = 0):
        worksheet = self._get_worksheet(worksheet_ix)
        try:
            worksheet.append_row(values=values)
        except Exception:
            logger.exception(f"GoogleSpreadsheet: failed to append row: {values}")
