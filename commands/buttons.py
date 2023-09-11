from aiogram import types

buttons_cancel = [
    [
        types.KeyboardButton(text="Cancel"),
    ]
]

buttons_share_profile = [
    [
        types.KeyboardButton(request_contact=True, text="Share number"),
    ]
]

buttons_start = [
    [
        types.KeyboardButton(text="Here"),
        types.KeyboardButton(text="Website"),
    ]
]

buttons_correct_edit = [
    [
        types.KeyboardButton(text="Correct"),
        types.KeyboardButton(text="Edit"),
    ]
]
