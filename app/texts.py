from aiogram import html


def start_text(user_name: str) -> str:
    return (
        f"Hello, {html.bold(user_name)}!\n\n"
        "Welcome to the bot. It will help you track your mood!\n\n"
        "Here you can:\n"
        "• Do X\n"
        "• Do Y\n"
        "• Do Z\n"
    )


def eneregy_level_text() -> str:
    return (
        "Оцените вашу энергию:\n\n"
        "Высокая — чувствую себя бодро и энергично, есть силы на учебу/работу/творчество\n\n"
        "Средняя — чувствую себя нейтрально/спокойно, без сильного прилива энергии\n\n"
        "Низкая — чувствую себя подавленно и устало, нет ни на что сил"
    )


def mood_factor_text() -> str:
    return (
        "Какой фактор сильнее всего повлиял на ваше настроение сегодня?\n\n"
        "Выберите один вариант."
    )


def mood_factor_other_text() -> str:
    return (
        "Напишите коротко, какая именно причина сильнее всего "
        "повлияла на ваше настроение сегодня."
    )


def day_change_wish_text() -> str:
    return "Хотелось ли вам сегодня что-то изменить в своём дне?"


def day_change_wish_other_text() -> str:
    return "Напишите коротко, как бы вам хотелось изменить сегодняшний день."
