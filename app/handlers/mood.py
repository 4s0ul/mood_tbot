from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.adapters.mood_spreadsheet import MoodSpreadsheet
from app.callbacks import (
    EmotionCallback,
    EnergyLevelCallback,
    MoodFactorCallback,
    MoodScoreCallback,
)
from app.keyboards import (
    MOOD_FACTOR_LABELS,
    emotions_keyboard,
    energy_keyboard,
    mood_factor_keyboard,
    mood_score_keyboard,
)
from app.models import MoodResult
from app.states import MoodState
from app.texts import eneregy_level_text, mood_factor_other_text, mood_factor_text

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
) -> None:
    data = await state.get_data()
    selected: list[str] = data.get("emotions", [])

    if not selected:
        await callback.answer("Выберите хотя бы одну эмоцию", show_alert=True)
        return

    await callback.answer()
    await state.set_state(MoodState.waiting_for_main_factor)

    if isinstance(callback.message, Message):
        await callback.message.edit_text("Понял. Эмоции сохранены.")
        await callback.message.answer(
            mood_factor_text(),
            reply_markup=mood_factor_keyboard(),
        )


@router.callback_query(
    MoodState.waiting_for_main_factor,
    MoodFactorCallback.filter(),
)
async def save_main_factor(
    callback: CallbackQuery,
    callback_data: MoodFactorCallback,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    code = callback_data.code

    if code == "other":
        await callback.answer()
        await state.set_state(MoodState.waiting_for_main_factor_comment)

        if isinstance(callback.message, Message):
            await callback.message.edit_text("Понял. Ты выбрал(а): Другое.")
            await callback.message.answer(mood_factor_other_text())
        return

    factor_text = MOOD_FACTOR_LABELS[code]

    await state.update_data(mood_factor=factor_text)
    data = await state.get_data()
    mood_result = MoodResult(**data)

    await mood_ss.write_mood_result(mood_result)
    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.edit_text(f"Понял. Фактор сохранён: {factor_text}")

    await state.clear()


@router.message(MoodState.waiting_for_main_factor_comment)
async def save_main_factor_comment(
    message: Message,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    text = (message.text or "").strip()

    if not text:
        await message.answer("Напиши коротко, что именно повлияло на настроение.")
        return

    await state.update_data(mood_factor=text)
    data = await state.get_data()
    mood_result = MoodResult(**data)

    await mood_ss.write_mood_result(mood_result)
    await message.answer("Понял. Причина сохранена.")

    await state.clear()
