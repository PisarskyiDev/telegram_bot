from aiogram.types import Message


def get_clear_data(message: Message) -> dict:
    data = {
        "URL": "",
        "email": "",
        "password": "",
    }
    entities = message.entities
    for item in entities:
        for item.type in data.keys():
            data[item.type] = item.extract_from(message.text)

    return data
