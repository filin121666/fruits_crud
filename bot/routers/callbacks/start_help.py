from aiogram import F, types, Router
from utils.outputs.help import send_help_from_callback

router = Router()


# FIXME:
@router.callback_query(F.data == "help")
async def callback_for_help(callback: types.CallbackQuery):
    await send_help_from_callback(callback=callback)
    await callback.answer()
