from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.admin.aschedule import send_message
from bot.admin.command import Commands
from bot.buttons import keyboard
from bot.filter.admin_filter import Admin, NoAdmin
from bot.filter.commands_filter import FoundCommand
from bot.filter.contact_filter import FilterContact
from bot.states.state import AllStates
from db import models
from db.engine import session
from db.orm import UserORM

main = Router()


@main.message(F.text.lower() == "cancel")
async def cancel(message: Message, state: FSMContext) -> None:
    """
    Cancels the current operation.

    Args:
        message (Message): The message object that triggered the cancellation.
        state (FSMContext): The state of the current conversation.

    Returns:
        None
    """
    kb = (
        keyboard.default_kb_super_admin
        if message.from_user.username == "Pisarskyi"
        else keyboard.default_kb
    )
    await message.answer("Cancelled", reply_markup=kb)
    await state.set_state(AllStates.login)


@main.message(F.text.lower() == "reset")
@main.message(Command("reset"))
async def reset_handler(message: Message, state: FSMContext) -> None:
    """
    Handles the reset command by resetting the state and sending a success message.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The FSM context object.

    Returns:
        None
    """

    kb = keyboard.start_kb

    await message.answer(
        "Reset was successful!",
        reply_markup=kb,
    )

    await state.clear()


@main.message(F.text.lower() == "start")
@main.message(Command("start"))
async def start_handler(message: Message, state: FSMContext) -> None:
    """
    Handle the "start" command or message.

    Args:
        message (Message): The message object received.
        state (FSMContext): The state of the conversation.

    Returns:
        None
    """

    await message.answer(
        "Please share your number to login in bot",
        reply_markup=keyboard.share_kb,
    )
    await state.set_state(AllStates.no_login)


@main.message(FilterContact())
async def login_handler(message: Message, state: FSMContext) -> None:
    """
    Decorates the login_handler function as a message handler for the FilterContact filter.
    Handles the login process by checking the user's state and ownership of the contact number.
    Updates the state based on the validation result and sends a response message.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The state machine context.

    Returns:
        None: This function does not return anything.
    """

    kb = (
        keyboard.default_kb_super_admin
        if message.from_user.username == "Pisarskyi"
        else keyboard.default_kb
    )

    check_state = await state.get_state()
    check_owner = await FilterContact.check_id(message)

    if check_state == AllStates.login:
        text = "You are already logged in!"
    else:
        if not check_owner:
            text = "Number was not confirmed! You can use only your own number"
            await state.set_state(AllStates.no_login)

        else:
            result = await UserORM(models.Users, message=message).register()
            if result and isinstance(result, str):
                await state.set_state(AllStates.login)
                text = result
            elif result and isinstance(result, bool):
                text = (
                    "Number confirmed successfully! Your account was created :) "
                    "\nNow you can use this bot"
                )
                await state.set_state(AllStates.login)
            else:
                text = (
                    "Number confirmed successfully! "
                    "But your account was not created! "
                    "\nPlease try again"
                )
    await message.reply(text, reply_markup=kb)


@main.message(F.text.lower() == "profile", AllStates.login)
async def get_profile(message: Message) -> None:
    """
    Decorator for handling the 'profile' command.

    This function is decorated with `@main.message(F.text.lower() == "profile", AllStates.login)`,
    which means it will be called when the user sends a message with the content 'profile' while in the 'login' state.

    Parameters:
    - message: The incoming message object.

    Returns:
    - None
    """

    user = await UserORM(message=message).select_user(
        user_id=message.from_user.id
    )
    await message.reply(
        "Your profile:"
        f"\nName: {user.name}"
        f"\nUsername: @{user.username}"
        f"\nPhone number: +{user.phone}"
        f"\nId: {user.id}"
        f"\nAdmin: {user.admin}",
    )


@main.message(FoundCommand(), NoAdmin())
async def check_admin_rights(message: types.Message) -> None:
    """
    Check if the user has admin rights and reply with a message if they do not.

    Parameters:
        message (types.Message): The message object.

    Returns:
        None
    """

    await message.reply("You dont have admin rights for doing that")


@main.message(F.text.lower() == "add admin", Admin())
async def give_admin(message: Message, state: FSMContext) -> None:
    """
    A decorator function that sets the message handler for the command "add admin" to the given function `give_admin`.
    The function `give_admin` takes two parameters: `message` of type `Message` and `state` of type `FSMContext`.
    The function does not return anything (`None`).
    When the command "add admin" is received, the function sends
    a reply message to the user with the text "Send username to GIVE him admin rights"
    and sets the state to `waiting_for_give` in the `FSMContext` object.
    """

    await message.reply("Send username to GIVE him admin rights")
    await state.set_state(AllStates.name_for_give)


@main.message(F.text.lower() == "del admin", Admin())
async def take_admin(message: Message, state: FSMContext) -> None:
    """
    A decorator function that takes a message, state, and checks
    if the text is equal to "del admin". If it is, it calls the Admin() function.

    Args:
        message (Message): The message object that contains the text.
        state (FSMContext): The state object that manages the state of the conversation.

    Returns:
        None
    """

    await message.reply("Send username to TAKE him admin rights")
    await state.set_state(AllStates.name_for_take)


@main.message(F.text.lower() == "all users", Admin())
async def call_all_users(message: Message, state: FSMContext) -> None:
    """
    Calls the `all_users` command if the user's message is "All users".

    Parameters:
        message (Message): The message object received from the user.
        state (FSMContext): The state object used for storing the conversation state.

    Returns:
        None
    """

    await Commands.all_users(message, state)


@main.message(F.text.lower() == "battery power", Admin())
async def call_battery_power(message: Message) -> None:
    """
    A decorator that checks if the text in the message is equal to "battery power" in lowercase.
    If the condition is met, it calls the `battery_power` method from the `Commands` class,
    passing in the `message` and `session` parameters.

    Parameters:
        message (Message): The message object received.

    Returns:
        None
    """

    response = await Commands.battery_power(message, session)
    if response == "unavailable":
        await message.reply("Battery is unavailable now")


@main.message(F.text.lower() == "all schedule", Admin())
async def call_all_schedule(message: Message, state: FSMContext) -> None:
    response = await Commands.check_schedule_users(message=message)
    for user in response:
        send_message(message_text=user, chat_id=message.chat.id)


@main.message(F.text.lower() == "add schedule", Admin())
async def activate_schedule(message: Message, state: FSMContext) -> None:
    await message.reply("Send username to add him to the Schedule")
    await state.set_state(AllStates.name_for_activate_schedule)


@main.message(F.text.lower() == "del schedule", Admin())
async def deactivate_schedule(message: Message, state: FSMContext) -> None:
    await message.reply("Send username to del him from the Schedule")
    await state.set_state(AllStates.name_for_deactivate_schedule)


@main.message(F.text.lower() == "ban user", Admin())
async def call_ban_user(message: Message, state: FSMContext) -> None:
    await message.reply("Send username to ban him")
    await state.set_state(AllStates.name_for_ban_user)


@main.message(F.text.lower() == "unban user", Admin())
async def call_unban_user(message: Message, state: FSMContext) -> None:
    await message.reply("Send username to unban him")
    await state.set_state(AllStates.name_for_unban_user)


@main.message(AllStates.name_for_ban_user)
async def waiting_for_ban_user(
    message: Message,
    state: FSMContext,
):
    response = await Commands.ban_user(message=message, ban=True)
    if response:
        await message.reply(f"User - {message.text} banned")
    await state.set_state(AllStates.login)


@main.message(AllStates.name_for_unban_user)
async def waiting_for_unban_user(
    message: Message,
    state: FSMContext,
):
    response = await Commands.ban_user(message=message, ban=False)
    if response:
        await message.reply(f"User - {message.text} unbanned")
    await state.set_state(AllStates.login)


@main.message(AllStates.name_for_activate_schedule)
async def waiting_for_activate_schedule(
    message: Message,
    state: FSMContext,
):
    response = await Commands.change_schedule(message, activate=True)
    await state.set_state(AllStates.login)
    if response:
        await message.reply("Schedule activated for this user")
    else:
        await message.reply("Something went wrong, maybe user not found")


@main.message(AllStates.name_for_deactivate_schedule)
async def waiting_for_deactivate_schedule(
    message: Message,
    state: FSMContext,
):
    response = await Commands.change_schedule(message, activate=False)
    await state.set_state(AllStates.login)
    if response:
        await message.reply("Schedule deactivated for this user")
    else:
        await message.reply("Something went wrong, maybe user not found")


@main.message(AllStates.name_for_take)
async def waiting_for_take(
    message: Message,
    state: FSMContext,
) -> None:
    """
    An asynchronous function that handles the 'waiting_for_take' state in the FSM.

    Args:
        message (Message): The message object containing the user's input.
        state (FSMContext): The context object for the FSM.

    Returns:
        None

    Raises:
        None
    """

    await message.reply("Please wait...")
    response = await Commands.del_admin(message, state)
    if response is None:
        await message.reply("Something went wrong, maybe user not found")


@main.message(AllStates.name_for_give)
async def waiting_for_give(message: Message, state: FSMContext) -> None:
    """
    Asynchronously handles the 'waiting_for_give' state in the FSM (Finite State Machine).

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The current state of the FSM.

    Returns:
        None

    Raises:
        None
    """

    await message.reply("Please wait...")
    response = await Commands.add_admin(message, state)
    if response is None:
        await message.reply("Something went wrong, maybe user not found")
    await state.set_state(AllStates.login)
