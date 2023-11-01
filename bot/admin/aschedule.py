import asyncio
import datetime

import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.admin.command import Commands
from db.orm import ScheduleORM
from settings.config import TOKEN

battery_power = Commands.battery_power
list_users = None
last_state = 0


def send_message(message_text, chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": message_text}
    requests.get(url, params=params)


async def schedule_check_status_battery() -> None:
    global list_users
    global last_state

    if list_users is None:
        list_users = await ScheduleORM().get_schedule_users()

    send_by_percents = [100, 90, 80, 70, 60, 50, 30, 20, 10, 5]
    response = await battery_power()

    if response == "unavailable":
        print(f"battery is unavailable now - {datetime.datetime.now()}")
        pass

    else:
        percent = int(response[1])
        current_voltage = float(response[0])

        if percent in send_by_percents and last_state != percent:
            for user in list_users:
                if percent <= 10:
                    message = f"КРИТИЧЕСКИЙ уровень заряда: {percent}%\nНапряжение батарей: {current_voltage}V"
                    print(
                        f"КРИТИЧЕСКИЙ уровень заряда: {percent}%\nНапряжение батарей: "
                        f"{current_voltage}V - {datetime.datetime.now()}"
                    )
                else:
                    message = f"Уровень заряда: {percent}%\nНапряжение батарей: {current_voltage}V"
                    print(
                        f"Уровень заряда: {percent}%\nНапряжение батарей: "
                        f"{current_voltage}V - {datetime.datetime.now()}"
                    )
                send_message(message, chat_id=user)
            last_state = percent


async def start_schedule():
    scheduler = AsyncIOScheduler(_event_loop=asyncio.get_event_loop())
    scheduler.add_job(
        schedule_check_status_battery,
        "interval",
        seconds=10,
    )
    scheduler.start()
