from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start = State()
    registration = State()
    logged_in = State()
    no_login = State()
    enter_email = State()
    confirm_email = State()
    before_finish = State()
    successful = State()
    login_gpt_on = State()
    login_gpt_off = State()
    error = State()
    check_login = State()
