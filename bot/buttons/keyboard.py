from aiogram import types

reset = [
    [
        types.KeyboardButton(text="Reset"),
    ]
]
cancel = [
    [
        types.KeyboardButton(text="Cancel"),
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
        types.KeyboardButton(text="Battery power"),
    ]
]

super_admin = [
    [
        types.KeyboardButton(text="Add admin"),
        types.KeyboardButton(text="Del admin"),
        types.KeyboardButton(text="Ban user"),
        types.KeyboardButton(text="Unban user"),
        types.KeyboardButton(text="Add schedule"),
        types.KeyboardButton(text="Del schedule"),
        types.KeyboardButton(text="All users"),
        types.KeyboardButton(text="All schedule"),
    ]
]

banned = [
    [
        types.KeyboardButton(text="OK"),
    ]
]


def build(buttons):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, selective=True
    )
    return keyboard


# default_kb = build(profile + reset)
default_kb_super_admin = build(
    super_admin + cancel + battery_power + profile + reset
)
default_kb = build(battery_power + profile + reset)
start_kb = build(start)
share_kb = build(share)
banned_kb = build(banned)
