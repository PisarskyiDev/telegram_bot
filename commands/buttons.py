from aiogram import types

buttons_start = [
    [
        types.KeyboardButton(text="Here"),
        types.KeyboardButton(text="Website"),
        types.KeyboardButton(request_contact=True, text="Share profile"),
    ]
]

buttons_yes_no = [
    [
        types.KeyboardButton(text="Correct"),
        types.KeyboardButton(text="Edit"),
    ]
]
