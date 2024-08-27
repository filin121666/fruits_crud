from aiogram import Router, types
from aiogram.filters.command import Command
from utils.outputs.help import send_help_from_message

router = Router()


@router.message(Command("help"))
async def help_handle(message: types.Message):
    await send_help_from_message(message=message)
