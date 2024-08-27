from aiogram.filters.command import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from ..states import GetFirstFruitsForm
import utils.requests.fruits as requests
from utils.outputs.fruits_list import send_fruits_list


router = Router()


@router.message(Command("get_first_fruits"))
async def get_first_fruits_handle(message: types.Message, state: FSMContext):
    await message.answer("Сколько первых фруктов Вы хотите получить?")
    await state.set_state(GetFirstFruitsForm.count)


@router.message(GetFirstFruitsForm.count)
async def process_first_fruits_count(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)
    except ValueError:
        await message.answer(text="Количество должно быть числом. Попробуйте снова.")
        return
    
    status, data = await requests.get_first_fruits(count=count)
    
    if status == 200:
        await send_fruits_list(message=message, fruits_list=data)
    elif status == 404 and data.get("detail", False)=="No fruit found":
        await message.answer("Фрукты не найдены :(")
    await state.clear()
