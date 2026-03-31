from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.adapters.mood_spreadsheet import MoodSpreadsheet

router = Router()


@router.message(Command("mood"))
async def mood_handler(message: Message, mood_ss: MoodSpreadsheet) -> None:
    await message.answer("How's your mood on a scale of 1 to 5?")
    # mood_result = MoodResult(mood_score=smth)
