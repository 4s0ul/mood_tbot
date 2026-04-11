from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.adapters.mood_spreadsheet import MoodSpreadsheet
from app.callbacks import EmotionCallback, EnergyLevelCallback, MoodScoreCallback
from app.keyboards import (
    emotions_keyboard,
    energy_keyboard,
    mood_score_keyboard,
)
from app.models import MoodResult
from app.states import MoodState
from app.texts import eneregy_level_text

router = Router()


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

    await state.update_data(
        username=callback.from_user.username or "",
        fullname=callback.from_user.full_name,
        tg_id=callback.from_user.id,
        mood_score=callback_data.score,
    )
    await state.set_state(MoodState.waiting_for_energy)

    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            f"Got it. Your mood today: {callback_data.score}/5"
        )
        await callback.message.answer(
            eneregy_level_text(),
            reply_markup=energy_keyboard(),
        )


@router.callback_query(MoodState.waiting_for_energy, EnergyLevelCallback.filter())
async def save_energy(
    callback: CallbackQuery,
    callback_data: EnergyLevelCallback,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.update_data(
        energy_level=callback_data.level,
        emotions=[],
    )
    await state.set_state(MoodState.waiting_for_emotions)

    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            f"Понял. Сегодня ваша энергия: {callback_data.level}"
        )
        await callback.message.answer(
            "3. Какие эмоции вы испытали сегодня?\nМожно выбрать несколько вариантов.",
            reply_markup=emotions_keyboard(),
        )


@router.callback_query(
    MoodState.waiting_for_emotions,
    EmotionCallback.filter(F.action == "toggle"),
)
async def toggle_emotion(
    callback: CallbackQuery,
    callback_data: EmotionCallback,
    state: FSMContext,
) -> None:
    await callback.answer()

    data = await state.get_data()
    selected: list[str] = data.get("emotions", [])
    code = callback_data.code

    if code in selected:
        selected = [item for item in selected if item != code]
    else:
        selected = [*selected, code]

    await state.update_data(emotions=selected)

    if isinstance(callback.message, Message):
        await callback.message.edit_reply_markup(
            reply_markup=emotions_keyboard(selected),
        )


@router.callback_query(
    MoodState.waiting_for_emotions,
    EmotionCallback.filter(F.action == "done"),
)
async def finish_emotions(
    callback: CallbackQuery,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    data = await state.get_data()
    selected: list[str] = data.get("emotions", [])

    if not selected:
        await callback.answer("Выберите хотя бы одну эмоцию", show_alert=True)
        return

    await callback.answer()

    mood_result = MoodResult(**data)
    await mood_ss.write_mood_result(mood_result)

    if isinstance(callback.message, Message):
        await callback.message.edit_text("Понял. Эмоции сохранены.")

    await state.clear()
