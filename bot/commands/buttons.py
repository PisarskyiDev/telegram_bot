from aiogram import types

cancel = [
    [
        types.KeyboardButton(text="Cancel"),
    ]
]

share_profile = [
    [
        types.KeyboardButton(request_contact=True, text="Share number"),
    ]
]

start = [
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
