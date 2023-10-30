from aiogram import types

reset = [
    [
        types.KeyboardButton(text="Reset"),
    ]
]

start = [
    [
        types.KeyboardButton(text="Start"),
    ]
]

share = [
    [
        types.KeyboardButton(text="Share", request_contact=True),
    ]
]


profile = [
    [
        types.KeyboardButton(text="Profile"),
    ]
]

battery_power = [
    [
        types.KeyboardButton(text="! Battery power"),
    ]
]


def build(buttons):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    return keyboard


default_kb = build(profile + reset)
start_kb = build(battery_power + start + reset)
