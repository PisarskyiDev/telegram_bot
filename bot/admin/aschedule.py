import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from bot.admin.command import Commands
from db.orm import select_user

battery_power = Commands.battery_power


def schedule_check_status_battery() -> None:
    from run import bot

    elena_user = asyncio.run(select_user(username="voskresenska_l"))
    nastya_user = asyncio.run(select_user(username="a_voskrecenskaya"))
    roman_user = asyncio.run(select_user(username="Pisarskyi"))
    list_users = [roman_user, elena_user, nastya_user]
    send_by_percents = [85, 70, 55, 25, 10, 5]

    response = asyncio.run(battery_power())
    if response == "unavailable":
        pass

    else:
        for user in list_users:
            if response and response[1] in send_by_percents:
                if response[1] == 10:
                    message = f"КРИТИЧЕСКИЙ уровень заряда: {response[1]}%\nНапряжение батарей: {response[0]}V"
                else:
                    message = f"Уровень заряда: {response[1]}%\nНапряжение батарей: {response[0]}V"
                asyncio.run(bot.send_message(chat_id=user.id, text=message))


def task():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_check_status_battery, "interval", seconds=3)
    scheduler.start()
