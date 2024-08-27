from aiogram.filters.command import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from ..states import CreateFruitForm
import utils.requests.fruits as requests
from utils.outputs.fruit_one import send_one_fruit
from utils.keyboards.yes_or_no import yes_or_no_keyboard_markup

router = Router()


@router.message(Command("create_fruit"))
async def create_fruit_handle(message: types.Message, state: FSMContext):
    await message.answer(text="Какое название будет у вашего этого фрукта?")
    await state.set_state(CreateFruitForm.title)


@router.message(CreateFruitForm.title)
async def process_create_fruit_title(message: types.Message, state: FSMContext):
    if not(message.text):
        await message.answer(text="Название не может являться пустым. Попробуйте снова.")
        return
    elif len(message.text) > 64:
        await message.answer(text="Название не может быть длиннее 64 символов. Попробуйте снова.")
        return
    
    await state.update_data(title=message.text)
    await state.set_state(CreateFruitForm.price)
    await message.answer(text="Сколько будет стоить этот фрукт (нужно число большее или равное нулю)?")


@router.message(CreateFruitForm.price)
async def process_create_fruit_price(message: types.Message, state: FSMContext):
    try:
        value = int(message.text)
        if value < 0:
            raise ValueError("The price should be positive.")
    except ValueError:
        await message.answer(text="Цена должна быть числом и больше или равна нулю. Попробуйте снова.")
        return
    
    await state.update_data(price=value)
    await state.set_state(CreateFruitForm.description_choice)
    await message.answer(text="Хотите ли Вы добавить описание для фрукта? (да или нет)", reply_markup=yes_or_no_keyboard_markup)



@router.message(CreateFruitForm.description_choice)
async def process_create_fruit_description_choice(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.set_state(CreateFruitForm.description)
        await message.answer(text="Напишите описание фрукта:")
    elif message.text.lower() == "нет":
        await state.update_data(description=None)
        state_data = await state.get_data()
        fruit = {
            "title": state_data.get("title"),
            "price": state_data.get("price"),
            "description": ""
        }
        status, data = await requests.create_fruit(fruit=fruit)
        if status == 201:
            await send_one_fruit(message=message, fruit=data)
        elif status == 400 and data.get("detail", False) == "A fruit with that title already exists":
            await message.answer(text="Ошибка! Фрукт с таким названием уже существует.")
            await state.clear()
    else:
        await message.answer(text="Вы дали некорректный ответ. Попробуйте снова.")
        return


@router.message(CreateFruitForm.description)
async def process_create_fruit_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    state_data: dict = await state.get_data()

    payload = {
        "title": state_data.get("title"),
        "price": state_data.get("price"),
        "description": message.text
    }

    status, data = await requests.create_fruit(fruit=payload)

    if status == 201:
        await message.answer("Созданный Вами фрукт:")
        await send_one_fruit(message=message, fruit=data)
    elif status == 400 and data.get("detail", False) == "A fruit with that title already exists":
        await message.answer(text="Ошибка! Фрукт с таким названием уже существует.")

    await state.clear()
