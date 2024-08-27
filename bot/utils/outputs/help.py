from aiogram import types
from aiogram.utils import markdown


HELP_TEXT = f"""{markdown.hbold("Мои команды:")}
/get_all_fruits - Получить все фрукты;
/get_first_fruits - Получить определённое количество фруктов;
/search_fruits - Найти фрукты по названию;
/create_fruit - Создать фрукт;
/full_update_fruit - Полностью обновить фрукт;
/partial_update_fruit - Частично обновить фрукт;
/delete_fruit - Удалить фрукт.
"""


async def send_help_from_message(message: types.Message):
    await message.answer(text=HELP_TEXT)


async def send_help_from_callback(callback: types.CallbackQuery):
    await callback.message.answer(text=HELP_TEXT)
