from datetime import date, datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

from app.adapters.mood_spreadsheet import MoodSpreadsheet
from app.callbacks import EnergyLevelCallback, MoodScoreCallback
from app.keyboards import energy_keyboard, mood_score_keyboard
from app.models import MoodResult
from app.states import MoodState

router = Router()


def build_mood_result(user: User, data: dict) -> MoodResult:
    return MoodResult(
        tg_id=user.id,
        username=user.username or "",
        name=user.full_name,
        date=date.today(),
        day_number=1,
        mood_score=data["mood_score"],
        emotions=data["energy_level"],
        daily_question="idk",
        daily_answer="idk",
        comment="idk",
        submitted_at=datetime.now(),
        # add your energy field here later if MoodResult has it
    )


@router.message(Command("mood"))
async def start_mood_flow(message: Message, state: FSMContext) -> None:
    await state.set_state(MoodState.waiting_for_mood)
    await message.answer(
        "How's your mood today?",
        reply_markup=mood_score_keyboard(),
    )


@router.callback_query(MoodState.waiting_for_mood, MoodScoreCallback.filter())
async def save_mood_score(
    callback: CallbackQuery,
    callback_data: MoodScoreCallback,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.update_data(mood_score=callback_data.score)
    await state.set_state(MoodState.waiting_for_energy)

    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            f"Got it. Your mood today: {callback_data.score}/5"
        )

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "Оцените вашу энергию:\n\n"
            "Высокая — чувствую себя бодро и энергично, есть силы на учебу/работу/творчество\n\n"
            "Средняя — чувствую себя нейтрально/спокойно, без сильного прилива энергии\n\n"
            "Низкая — чувствую себя подавленно и устало, нет ни на что сил",
            reply_markup=energy_keyboard(),
        )


@router.callback_query(MoodState.waiting_for_energy, EnergyLevelCallback.filter())
async def save_energy(
    callback: CallbackQuery,
    callback_data: EnergyLevelCallback,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    await callback.answer()

    await state.update_data(energy_level=callback_data.level)
    data = await state.get_data()

    mood_result = build_mood_result(callback.from_user, data)
    await mood_ss.write_mood_result(mood_result)

    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            f"Понял. Сегодня ваша энергия {callback_data.level}"
        )

    await state.clear()
