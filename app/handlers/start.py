from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards import main_menu_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(
        "Привет! Здесь ты можешь заполнить дневник эмоций или посмотреть практики.",
        reply_markup=main_menu_keyboard(),
    )
