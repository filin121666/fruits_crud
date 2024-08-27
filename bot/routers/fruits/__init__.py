from aiogram import Router
from .commands.get_first_fruits import router as get_first_fruits_router
from .commands.get_all_fruits import router as get_all_fruits_router
from .commands.create_fruit import router as create_fruit_router
from .commands.search_fruits import router as search_fruits_router
from .commands.full_update_fruit import router as full_update_fruit_router
from .commands.delete_fruit import router as delete_fruit_router
from .commands.partial_update_fruit import router as partial_update_fruit_router

router = Router()

router.include_routers(
    get_first_fruits_router,
    get_all_fruits_router,
    create_fruit_router,
    search_fruits_router,
    full_update_fruit_router,
    delete_fruit_router,
    partial_update_fruit_router,
)
