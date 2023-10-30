import asyncio

import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.admin.command import Commands
from db.orm import all_users, select_user
from settings.config import TOKEN

battery_power = Commands.battery_power
# list_users = asyncio.run(all_users())
list_users = [412740881]
last_state = 0


def send_message(message_text, chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": message_text}
    requests.get(url, params=params)


async def schedule_check_status_battery() -> None:
    global last_state
    send_by_percents = [100, 90, 80, 70, 60, 50, 30, 20, 10, 5]
    response = await battery_power()
    percent = int(response[1])
    current_voltage = float(response[0])
    if response == "unavailable":
        pass

    else:
        if percent in send_by_percents and last_state != percent:
            for user in list_users:
                if percent <= 10:
                    message = f"КРИТИЧЕСКИЙ уровень заряда: {percent}%\nНапряжение батарей: {current_voltage}V"
                else:
                    message = f"Уровень заряда: {percent}%\nНапряжение батарей: {current_voltage}V"
                # send_message(message, chat_id=user.id)
                send_message(message, chat_id=user)
            last_state = percent


async def start_schedule():
    scheduler = AsyncIOScheduler(_event_loop=asyncio.get_event_loop())
    scheduler.add_job(
        schedule_check_status_battery,
        "interval",
        seconds=10,
        start_date="2000-01-01 00:00:00",
    )
    scheduler.start()
