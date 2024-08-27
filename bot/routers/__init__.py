from aiogram import Router
from .fruits import router as fruits_router
from .main import router as main_router
from .callbacks import router as callbacks_router

router = Router()

router.include_routers(
    main_router,
    fruits_router,
    callbacks_router,
)
