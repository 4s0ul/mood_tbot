from datetime import date, datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from app.adapters.mood_spreadsheet import MoodSpreadsheet
from app.models import MoodResult


class MoodState(StatesGroup):
    waiting_for_mood = State()


router = Router()


@router.message(Command("mood"))
async def mood_handler(message: Message, state: FSMContext) -> None:
    await message.answer("How's your mood on a scale of 1 to 5?")
    await state.set_state(MoodState.waiting_for_mood)


@router.message(MoodState.waiting_for_mood)
async def process_mood(
    message: Message,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    try:
        score = int(message.text)
        if score < 1 or score > 5:
            raise ValueError
    except TypeError, ValueError:
        await message.answer("Please enter a number from 1 to 5.")
        return

    if not message.from_user or not message.from_user.username:
        raise ValueError

    mood_result = MoodResult(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        name=message.from_user.full_name,
        date=date.today(),
        day_number=1,
        mood_score=score,
        emotions="idk",
        daily_question="idk",
        daily_answer="idk",
        comment="idk",
        submitted_at=datetime.now(),
    )

    await message.answer(f"Got it! Your mood: {score}")

    mood_ss.write_mood_result(mood_result)

    await state.clear()
