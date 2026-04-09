from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks import EnergyLevelCallback, MoodScoreCallback


def mood_score_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    moods = {"depressed": 1, "ploho": 2, "norm": 3, "good": 4, "ya ahuennii": 5}
    for score in moods:
        builder.button(
            text=str(score),
            callback_data=MoodScoreCallback(score=moods[score]),
        )

    builder.adjust(1)
    return builder.as_markup()


def energy_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Высокая",
        callback_data=EnergyLevelCallback(level="high"),
    )
    builder.button(
        text="Средняя",
        callback_data=EnergyLevelCallback(level="medium"),
    )
    builder.button(
        text="Низкая",
        callback_data=EnergyLevelCallback(level="low"),
    )

    builder.adjust(1)
    return builder.as_markup()
