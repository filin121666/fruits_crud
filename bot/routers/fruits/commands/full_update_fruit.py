from aiogram.filters.command import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from ..states import FullUpdateFruitForm
import utils.requests.fruits as requests
from utils.outputs.fruit_one import send_one_fruit
from utils.keyboards.yes_or_no import yes_or_no_keyboard_markup

router = Router()


@router.message(Command("full_update_fruit"))
async def full_update_fruit_handle(message: types.Message, state: FSMContext):
    await message.answer(text="Фрукт с каким названием Вы хотите обновить?")
    await state.set_state(FullUpdateFruitForm.old_title)


@router.message(FullUpdateFruitForm.old_title)
async def process_full_update_fruit_old_fruit(message: types.Message, state: FSMContext):
    if not(message.text):
        await message.answer(text="Название не может являться пустым. Попробуйте снова.")
        return
    elif len(message.text) > 64:
        await message.answer(text="Название не может быть длиннее 64 символов. Попробуйте снова.")
        return
    
    await state.update_data(old_title=message.text)
    await state.set_state(FullUpdateFruitForm.new_title)
    await message.answer(text="Какое будет новое название у вашего фрукта?")


@router.message(FullUpdateFruitForm.new_title)
async def process_full_update_fruit_new_fruit(message: types.Message, state: FSMContext):
    if len(message.text) > 64:
        await message.answer(text="Название не может быть длиннее 64 символов. Попробуйте снова.")
        return

    await state.update_data(new_title=message.text)
    await state.set_state(FullUpdateFruitForm.new_price)
    await message.answer(text="Какая будет новая цена у вашего фрукта (нужно число большее или равное нулю)?")


@router.message(FullUpdateFruitForm.new_price)
async def process_full_update_fruit_new_price(message: types.Message, state: FSMContext):
    try:
        value = int(message.text)
        if value < 0:
            raise ValueError("The price should be positive.")
    except ValueError:
        await message.answer(text="Цена должна быть числом и больше или равна нулю. Попробуйте снова.")
        return
    
    await state.update_data(new_price=value)
    await state.set_state(FullUpdateFruitForm.new_description_choice)
    await message.answer(text="Хотите ли Вы добавить описание для фрукта? (да или нет)", reply_markup=yes_or_no_keyboard_markup)


@router.message(FullUpdateFruitForm.new_description_choice)
async def process_full_update_fruit_new_description_choice(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.set_state(FullUpdateFruitForm.new_description)
        await message.answer(text="Напишите описание фрукта:")
    elif message.text.lower() == "нет":
        await state.update_data(new_description=None)
        state_data = await state.get_data()
        fruit = {
                "old_title": state_data.get("old_title"),
                "new_title": state_data.get("new_title"),
                "new_price": state_data.get("new_price"),
                "new_description": ""
            }
        status, data = await requests.full_update_fruit_by_title(update_fruit=fruit)
        if status == 200:
            await send_one_fruit(message=message, fruit=data)
        elif status == 404 and data.get("detail", False) == "Not found, an incorrect old_title may have been entered":
            await message.answer(text="Фрукт с таким названием не найден. Изменения не были выполнены.")
            await state.clear()
    else:
        await message.answer(text="Вы дали некорректный ответ. Попробуйте снова.")
        return


@router.message(FullUpdateFruitForm.new_description)
async def process_full_update_fruit_new_description(message: types.Message, state: FSMContext):
    state_data: dict = await state.get_data()

    fruit = {
                "old_title": state_data.get("old_title"),
                "new_title": state_data.get("new_title"),
                "new_price": state_data.get("new_price"),
                "new_description": message.text
            }

    status, data = await requests.full_update_fruit_by_title(update_fruit=fruit)

    if status == 200:
        await message.answer("Ваши изменения:")
        await send_one_fruit(message=message, fruit=data)
    elif status == 404 and data.get("detail", False) == "Not found, an incorrect old_title may have been entered":
        await message.answer(text="Фрукт с таким названием не найден. Изменения не были выполнены.")

    await state.clear()
