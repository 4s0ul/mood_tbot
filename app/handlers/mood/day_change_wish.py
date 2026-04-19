from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.adapters.mood_spreadsheet import MoodSpreadsheet
from app.callbacks import (
    DayChangeWishCallback,
)
from app.keyboards import (
    DAY_CHANGE_WISH_LABELS,
)
from app.schemas import MoodResult
from app.states import MoodState
from app.texts import (
    day_change_wish_other_text,
)

router = Router()


@router.callback_query(
    MoodState.waiting_for_day_change_wish,
    DayChangeWishCallback.filter(),
)
async def save_day_change_wish(
    callback: CallbackQuery,
    callback_data: DayChangeWishCallback,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    code = callback_data.code

    if code == "other":
        await callback.answer()
        await state.set_state(MoodState.waiting_for_day_change_wish_comment)

        if isinstance(callback.message, Message):
            await callback.message.edit_text("Понял. Ты выбрал(а): Другое.")
            await callback.message.answer(day_change_wish_other_text())
        return

    day_change_wish_text_value = DAY_CHANGE_WISH_LABELS[code]

    await state.update_data(day_change_wish=day_change_wish_text_value)
    data = await state.get_data()
    mood_result = MoodResult(**data)

    await mood_ss.write_mood_result(mood_result)
    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            f"Понял. Желание изменить день сохранено: {day_change_wish_text_value}"
        )

    await state.clear()


@router.message(MoodState.waiting_for_day_change_wish_comment)
async def save_day_change_wish_comment(
    message: Message,
    state: FSMContext,
    mood_ss: MoodSpreadsheet,
) -> None:
    text = (message.text or "").strip()

    if not text:
        await message.answer("Напиши коротко, что хотелось бы изменить в своём дне.")
        return

    await state.update_data(day_change_wish=text)
    data = await state.get_data()
    mood_result = MoodResult(**data)

    await mood_ss.write_mood_result(mood_result)
    await message.answer("Понял. Ответ сохранён.")

    await state.clear()
