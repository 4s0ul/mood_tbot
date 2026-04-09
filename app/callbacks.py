from aiogram.filters.callback_data import CallbackData


class MoodScoreCallback(CallbackData, prefix="mood"):
    score: int


class EnergyLevelCallback(CallbackData, prefix="energy"):
    level: str
