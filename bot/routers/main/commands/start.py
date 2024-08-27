from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, Router


router = Router()


@router.message(Command("start"))
async def start_handle(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="help",
            callback_data="help",
        )
    )

    await message.answer(
        text="Здравствуйте, я бот, который поможет Вам работать с приложением Fruits_crud. Чтобы начать работу со мной, выбери команду из меню или нажми на help, чтобы получить список команд",
        reply_markup=builder.as_markup(),
    )
