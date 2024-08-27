from aiogram import types, Router
from aiogram.filters.command import Command

import utils.requests.fruits as requests
from utils.outputs.fruits_list import send_fruits_list

router = Router()

@router.message(Command("get_all_fruits"))
async def get_all_fruits_handle(message: types.Message):
    status, data = await requests.get_all_fruits()
    if status == 200:
        await send_fruits_list(message=message, fruits_list=data)
    elif status == 404 and data.get("detail", False)=="No fruit found":
        await message.answer(text="Фрукты не найдены :(")
