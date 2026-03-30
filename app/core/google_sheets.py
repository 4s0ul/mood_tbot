from collections.abc import Sequence
from pathlib import Path

import gspread
from gspread import Worksheet


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


class GoogleSheets:
    def __init__(self, creds_path: Path, g_spread_key: str) -> None:
        self.gc = gspread.service_account(filename=creds_path)
        self.spread = self.gc.open_by_key(g_spread_key)
        self._worksheets: WorksheetsCache | None = None

    def _get_worksheet(self, worksheet_ix) -> Worksheet:
        if not self._worksheets:
            self._worksheets = WorksheetsCache()
        worksheet = self._worksheets.get_worksheet(worksheet_ix)
        if not worksheet:
            worksheet = self.spread.get_worksheet(worksheet_ix)
            self._worksheets.add_worksheet(worksheet_ix, worksheet)
        return worksheet

    def append_row(self, values: Sequence, worksheet_ix: int = 0):
        worksheet = self._get_worksheet(worksheet_ix)
        worksheet.append_row(values=values)
