from aiogram.filters.command import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from ..states import PartialUpdateFruitForm
import utils.requests.fruits as requests
from utils.outputs.fruit_one import send_one_fruit
from utils.keyboards.yes_or_no import yes_or_no_keyboard_markup

router = Router()


@router.message(Command("partial_update_fruit"))
async def partial_update_fruit_handle(message: types.Message, state: FSMContext):
    await message.answer(text="Фрукт с каким названием Вы хотите обновить?")
    await state.set_state(PartialUpdateFruitForm.old_title)


@router.message(PartialUpdateFruitForm.old_title)
async def process_partial_update_fruit_old_title(message: types.Message, state: FSMContext):
    if not(message.text):
        await message.answer(text="Название не может являться пустым. Попробуйте снова.")
        return
    elif len(message.text) > 64:
        await message.answer(text="Название не может быть длиннее 64 символов. Попробуйте снова.")
        return
    
    await state.update_data(old_title=message.text)
    await state.set_state(PartialUpdateFruitForm.new_title_update_choice)
    await message.answer(text="Хотите ли Вы изменить название? (да или нет)", reply_markup=yes_or_no_keyboard_markup)


@router.message(PartialUpdateFruitForm.new_title_update_choice)
async def process_partial_update_fruit_new_title_choice_update(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.set_state(PartialUpdateFruitForm.new_title)
        await message.answer(text="Какое будет новое название у фрукта?")
    elif message.text.lower() == "нет":
        await state.update_data(new_title=False)
        await state.set_state(PartialUpdateFruitForm.new_price_update_choice)
        await message.answer(text="Хотите ли Вы изменить цену? (да или нет)", reply_markup=yes_or_no_keyboard_markup)


@router.message(PartialUpdateFruitForm.new_title)
async def process_partial_update_fruit_new_title(message: types.Message, state: FSMContext):
    if len(message.text) > 64:
        await message.answer(text="Название не может быть длиннее 64 символов. Попробуйте снова.")
        return

    await state.update_data(new_title=message.text)
    await state.set_state(PartialUpdateFruitForm.new_price_update_choice)
    await message.answer(text="Хотите ли Вы изменить цену? (да или нет)", reply_markup=yes_or_no_keyboard_markup)


@router.message(PartialUpdateFruitForm.new_price_update_choice)
async def process_partial_update_fruit_new_price_update_choice(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.set_state(PartialUpdateFruitForm.new_price)
        await message.answer(text="Какая будет новая цена у фрукта?")
    elif message.text.lower() == "нет":
        await state.update_data(new_price=False)
        await state.set_state(PartialUpdateFruitForm.new_description_update_choice)
        await message.answer(text="Хотите ли Вы изменить описание? (да или нет)", reply_markup=yes_or_no_keyboard_markup)


@router.message(PartialUpdateFruitForm.new_price)
async def process_partial_update_fruit_new_price(message: types.Message, state: FSMContext):
    try:
        value = int(message.text)
        if value < 0:
            raise ValueError("The price should be positive.")
    except ValueError:
        await message.answer(text="Цена должна быть числом и больше или равна нулю. Попробуйте снова.")
        return
    
    await state.update_data(new_price=value)
    await state.set_state(PartialUpdateFruitForm.new_description_update_choice)
    await message.answer(text="Хотите ли Вы изменить описание для фрукта? (да или нет)", reply_markup=yes_or_no_keyboard_markup)


@router.message(PartialUpdateFruitForm.new_description_update_choice)
async def process_partial_update_fruit_new_description_update_choice(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.set_state(PartialUpdateFruitForm.new_description_choice)
        await message.answer(text="Будет ли новое описание у фрукта? (да или нет)", reply_markup=yes_or_no_keyboard_markup)
    elif message.text.lower() == "нет":
        state_data = await state.get_data()
        payload = {
            "new_title": state_data.get("new_title"),
            "new_price": state_data.get("new_price"),
            "new_description": False
        }

        if not any(payload.values()):
            await message.answer(text="Изменения не были выполнены, так как Вы не внесли изменения.")
        else:
            payload["old_title"] = state_data.get("old_title")
            status, data = await requests.partial_update_fruit_by_title(update_fruit=payload)
            if status == 200:
                await message.answer(text="Ваши изменения:")
                await send_one_fruit(message=message, fruit=data)
            elif status == 404 and data.get("detail", False) == "Not found, an incorrect <old_title> may have been entered":
                await message.answer(text="Фрукт с таким названием не найден. Изменения не были выполнены.")
        await state.clear()


# Не доделано
@router.message(PartialUpdateFruitForm.new_description_choice)
async def process_partial_update_fruit_new_description_choice(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.set_state(PartialUpdateFruitForm.new_description)
        await message.answer(text="Какое будет новое описание у фрукта?")
    elif message.text.lower() == "нет":
        state_data = await state.get_data()
        payload = {
            "old_title": state_data.get("old_title"),
            "new_title": state_data.get("new_title"),
            "new_price": state_data.get("new_price"),
            "new_description": ""
        }
        status, data = await requests.partial_update_fruit_by_title(update_fruit=payload)
        if status == 200:
            await message.answer(text="Ваши изменения:")
            await send_one_fruit(message=message, fruit=data)
        elif status == 404 and data.get("detail", False) == "Not found, an incorrect <old_title> may have been entered":
            await message.answer(text="Фрукт с таким названием не найден. Изменения не были выполнены.")
        await state.clear()


@router.message(PartialUpdateFruitForm.new_description)
async def process_partial_update_fruit_new_description(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    payload = {
        "old_title": state_data.get("old_title"),
        "new_title": state_data.get("new_title"),
        "new_price": state_data.get("new_price"),
        "new_description": message.text
    }
    status, data = await requests.partial_update_fruit_by_title(update_fruit=payload)
    if status == 200:
        await message.answer(text="Ваши изменения:")
        await send_one_fruit(message=message, fruit=data)
    elif status == 404 and data.get("detail", False) == "Not found, an incorrect <old_title> may have been entered":
        await message.answer(text="Фрукт с таким названием не найден. Изменения не были выполнены.")
    await state.clear()
