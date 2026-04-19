from aiogram.filters.callback_data import CallbackData


class MoodScoreCallback(CallbackData, prefix="mood"):
    score: int


class EnergyLevelCallback(CallbackData, prefix="energy"):
    level: str


class EmotionCallback(CallbackData, prefix="emotion"):
    action: str
    code: str


class MoodFactorCallback(CallbackData, prefix="factor"):
    code: str


class DayChangeWishCallback(CallbackData, prefix="factor"):
    code: str
