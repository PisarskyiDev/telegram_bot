from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.buttons import keyboard
from bot.states.state import AllStates
from db.orm import select_user


class Commands:
    @staticmethod
    async def battery_power(message: types.Message, state: FSMContext) -> None:
        await message.reply("Done! Battery is on!")

    @staticmethod
    async def admin_mode(
        message: types.Message,
        state: FSMContext,
    ) -> None:
        is_admin = await select_user(user_id=message.from_user.id)
        exist_state = await state.get_state()

        if exist_state == AllStates.login and is_admin.admin:
            await state.set_state(AllStates.admin_mode)
            admin_on_kb = keyboard.admin_on_kb
            await message.reply(
                "Admin mode is activated!", reply_markup=admin_on_kb
            )
            await state.set_state(AllStates.admin_mode)

        elif exist_state == AllStates.admin_mode:
            admin_off_kb = keyboard.default_kb
            await message.reply(
                "Admin mode is deactivated!", reply_markup=admin_off_kb
            )
            await state.set_state(AllStates.login)
        else:
            await message.reply(
                "You dont have admin rights",
                reply_markup=keyboard.default_kb,
            )


#
#
# def set_admin():
#     pass
#
#
# def del_admin():
#     pass
#
#
# def ban_user():
#     pass
#
#
# def unban_user():
#     pass
#
#
# def users_list():
#     pass
#
#
# def user_commands_list():
#     pass


variables = globals()
