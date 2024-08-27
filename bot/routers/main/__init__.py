from aiogram import Router
from .commands.start import router as start_router
from .commands.help import router as help_router

router = Router()

router.include_routers(
    start_router,
    help_router,
)
