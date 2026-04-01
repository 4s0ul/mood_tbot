from aiogram import Dispatcher

from app.handlers import echo, help, mood, start


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(mood.router)
    dp.include_router(echo.router)
