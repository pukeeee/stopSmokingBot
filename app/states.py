from aiogram.fsm.state import State, StatesGroup


class Setting(StatesGroup):
    setCigaretteCount = State()
    setCigarettePrice = State()