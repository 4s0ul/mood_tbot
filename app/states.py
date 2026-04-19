from aiogram.fsm.state import State, StatesGroup


class MoodState(StatesGroup):
    waiting_for_mood = State()
    waiting_for_energy = State()
    waiting_for_emotions = State()
    waiting_for_main_factor = State()
    waiting_for_main_factor_comment = State()
    waiting_for_day_change_wish = State()
    waiting_for_day_change_wish_comment = State()
