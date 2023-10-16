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
registration = [
    [
        types.KeyboardButton(text="Here"),
        types.KeyboardButton(text="Website"),
    ]
]

correct_edit = [
    [
        types.KeyboardButton(text="Correct"),
        types.KeyboardButton(text="Edit"),
    ]
]

registrate = [
    [
        types.KeyboardButton(text="Registrate"),
    ]
]

share = [
    [
        types.KeyboardButton(text="Share", request_contact=True),
    ]
]
login_check = [
    [
        types.KeyboardButton(text="Send"),
    ]
]

ai_on = [
    [
        types.KeyboardButton(text="Ai On"),
    ]
]

ai_off = [
    [
        types.KeyboardButton(text="Ai Off"),
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
