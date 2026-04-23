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


def mood_score_text() -> str:
    return "Какое у тебя сегодня настроение?"


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


def comment_decision_text() -> str:
    return "Хотите оставить комментарий по желанию?"


def comment_text_request() -> str:
    return "Напишите комментарий."


def no_daily_question_text() -> str:
    return "Сегодня вопроса дня нет."


def daily_questions_menu_text() -> str:
    return "Это меню для управления вопросами дня.\nЧто вы хотите сделать?"


def daily_question_date_text() -> str:
    return (
        "Введите дату, на которую должен быть активен вопрос.\n\n"
        "Формат: YYYY-MM-DD\n"
        "Например: 2026-04-22"
    )


def daily_question_text_text() -> str:
    return "Теперь отправьте сам вопрос дня."


def daily_question_cancelled_text() -> str:
    return "Действие отменено."


def practice_offer_text() -> str:
    return (
        "Вижу, что сегодня у тебя не самое лучшее настроение.\n"
        "Хочешь, я предложу тебе несколько практик?"
    )


def practices_list_text() -> str:
    return "У меня для тебя есть такие практики:"


def goodbye_text() -> str:
    return "Спасибо, что заполнил(а) дневник эмоций сегодня.\nХорошего тебе дня."


def goodbye_with_practice_text() -> str:
    return (
        "Надеюсь, эта практика тебе поможет.\n"
        "Ты молодец, что заполнил(а) дневник эмоций сегодня.\n"
        "Хорошего тебе дня."
    )
