from aiogram.fsm.state import StatesGroup, State


class StartUpStates(StatesGroup):
    start = State()
    no_login = State()
    check_login = State()


class RegistrationStates(StartUpStates):
    registration = State()
    already_registrate = State()


class AiStates(RegistrationStates):
    logged_ai_on = State()
    logged_ai_off = State()


class CheckoutStates(AiStates):
    check_login = State()
    enter_email = State()
    confirm_email = State()
    ready = State()


class ResultStates(CheckoutStates):
    error = State()
    successful = State()


class AllStates(ResultStates):
    reset = State()
