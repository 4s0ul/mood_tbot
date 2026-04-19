from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards import (
    mood_score_keyboard,
)
from app.states import MoodState

router = Router()


@router.message(Command("mood"))
async def start_mood_flow(message: Message, state: FSMContext) -> None:
    await state.set_state(MoodState.waiting_for_mood)
    await message.answer(
        "How's your mood today?",
        reply_markup=mood_score_keyboard(),
    )
