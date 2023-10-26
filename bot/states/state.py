from aiogram.fsm.state import StatesGroup, State


class AllStates(StatesGroup):
    start = State()
    reset = State()
    no_login = State()
    login = State()
    admin_mode = State()
    waiting_for_take = State()
    waiting_for_give = State()
