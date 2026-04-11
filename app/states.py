from aiogram.fsm.state import State, StatesGroup


class MoodState(StatesGroup):
    waiting_for_mood = State()
    waiting_for_energy = State()
    waiting_for_emotions = State()
