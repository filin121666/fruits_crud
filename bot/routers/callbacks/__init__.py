from aiogram import Router
from .start_help import router as start_help_router

router = Router()

router.include_router(router=start_help_router)
