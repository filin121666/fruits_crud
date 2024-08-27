from aiogram import types


yes_or_no_keyboard_markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )