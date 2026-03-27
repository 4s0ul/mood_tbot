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
