from aiogram.fsm.state import StatesGroup, State


class AllStates(StatesGroup):
    start = State()
    reset = State()
    no_login = State()
    login = State()
    name_for_take = State()
    name_for_give = State()
    name_for_activate_schedule = State()
    name_for_deactivate_schedule = State()
