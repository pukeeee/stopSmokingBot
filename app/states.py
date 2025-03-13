from aiogram.fsm.state import State, StatesGroup


class Setting(StatesGroup):
    setCigaretteCount = State()
    setCigarettePrice = State()


class Plan(StatesGroup):
    setPlanDate = State()
    setStartCigarettes = State()
    setEndCigarettes = State()