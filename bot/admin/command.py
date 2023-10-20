from aiogram import types


async def battery_power(message: types.Message) -> None:
    await message.reply("Done! Battery is on!")


# def admin_mode():
#     pass
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
