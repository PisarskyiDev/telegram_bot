from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start = State()
    registration = State()
    enter_email = State()
    confirm_email = State()
    before_finish = State()
    successful = State()
