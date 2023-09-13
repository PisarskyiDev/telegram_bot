from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    here = State()
    start = State()
    registration = State()
    enter_email = State()
    confirm_email = State()
    pass_email = State()
    before_finish = State()
    successful = State()
