from aiogram.filters.command import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from ..states import DeleteFruitForm
import utils.requests.fruits as requests
from utils.outputs.fruit_one import send_one_fruit


router = Router()


@router.message(Command("delete_fruit"))
async def delete_fruit_handle(message: types.Message, state: FSMContext):
    await message.answer(text="Фрукт с каким названием Вы хотите удалить?")
    await state.set_state(DeleteFruitForm.title)


@router.message(DeleteFruitForm.title)
async def process_delete_fruit_title(message: types.Message, state: FSMContext):
    if not(message.text):
        await message.answer(text="Название не может являться пустым. Попробуйте снова.")
        return
    elif len(message.text) > 64:
        await message.answer(text="Название не может быть длиннее 64 символов. Попробуйте снова.")
        return
    
    status, data = await requests.delete_fruit_by_title(title=message.text)

    if status == 200:
        await message.answer(text="Удалённый фрукт:")
        await send_one_fruit(message=message, fruit=data)
    elif status == 404 and data.get("detail", False) == "Not found, an incorrect title may have been entered":
        await message.answer(text="Фрукт с таким названием не найден. Удаление не было выполнено.")
    await state.clear()
