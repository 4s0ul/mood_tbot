from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks import (
    DayChangeWishCallback,
    EmotionCallback,
    EnergyLevelCallback,
    MoodFactorCallback,
    MoodScoreCallback,
)

EMOTION_LABELS: dict[str, str] = {
    "inspiration": "Воодушевление",
    "calm": "Спокойствие",
    "sadness": "Тоска / грусть",
    "anxiety": "Тревога / раздражение",
    "fatigue": "Усталость",
}


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


def emotions_keyboard(selected: list[str] | None = None) -> InlineKeyboardMarkup:
    selected_set = set(selected or [])
    builder = InlineKeyboardBuilder()

    for code, label in EMOTION_LABELS.items():
        prefix = "✓ " if code in selected_set else ""
        builder.button(
            text=f"{prefix}{label}",
            callback_data=EmotionCallback(action="toggle", code=code),
        )

    builder.button(
        text="Готово",
        callback_data=EmotionCallback(action="done", code="done"),
    )

    builder.adjust(1)
    return builder.as_markup()


MOOD_FACTOR_LABELS: dict[str, str] = {
    "social": "Общение с другими людьми",
    "work": "Учёба или работа",
    "inner": "Моё внутреннее состояние",
    "physical": "Физическое самочувствие",
    "event": "Какое-то конкретное событие",
    "other": "Другое",
}


def mood_factor_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for code, label in MOOD_FACTOR_LABELS.items():
        builder.button(
            text=label,
            callback_data=MoodFactorCallback(code=code),
        )

    builder.adjust(1)
    return builder.as_markup()


DAY_CHANGE_WISH_LABELS: dict[str, str] = {
    "alot": "Да, многое",
    "alittle": "Да, немногое",
    "allgood": "Нет, все устраивало",
    "noidea": "Затрудняюсь ответить",
    "other": "Другое",
}


def day_change_wish_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for code, label in DAY_CHANGE_WISH_LABELS.items():
        builder.button(
            text=label,
            callback_data=DayChangeWishCallback(code=code),
        )

    builder.adjust(1)
    return builder.as_markup()
