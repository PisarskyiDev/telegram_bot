from aiogram import types

reset = [
    [
        types.KeyboardButton(text="Reset"),
    ]
]

share_profile = [
    [
        types.KeyboardButton(request_contact=True, text="Share number"),
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


def keyboard_build(buttons, placeholder: str = "Which choose?"):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder=placeholder,
    )
    return keyboard
