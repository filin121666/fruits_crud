from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from ..states import SearchFruits
import utils.requests.fruits as requests
from utils.outputs.fruits_list import send_fruits_list_with_numeration


router = Router()

@router.message(Command("search_fruits"))
async def search_fruits_handle(message: types.Message, state: FSMContext):
    await message.answer(text="Введите Ваш запрос (название фруктов)")
    await state.set_state(SearchFruits.fruits_title)


@router.message(SearchFruits.fruits_title)
async def process_search_fruits_fruits_title(message: types.Message, state: FSMContext):
    if not(message.text):
        await message.answer(text="Ваш запрос не может являться пустым. Попробуйте снова.")
        return

    status, data = await requests.search_fruits_by_title(fruits_title=message.text)
    if status == 200:
        await message.answer(text="Результаты поиска:")
        await send_fruits_list_with_numeration(message=message, fruits_list=data)
    elif status == 404 and data.get("detail", False) == "No fruit found":
        await message.answer(text="Фрукты по данному запросу не найдены.")
    await state.clear()
