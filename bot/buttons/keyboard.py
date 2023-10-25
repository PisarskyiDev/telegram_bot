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


admin_off = [
    [
        types.KeyboardButton(text="! Admin OFF"),
    ]
]
admin_on = [
    [
        types.KeyboardButton(text="! Admin ON"),
    ]
]


def build(buttons):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    return keyboard


default_kb = build(profile + reset)
start_kb = build(start + reset)
admin_on_kb = build(admin_off + profile + reset)
