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
