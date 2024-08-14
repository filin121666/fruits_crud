from fastapi import APIRouter

from .fruits.views import router as fruit_router
from core.config import settings

router = APIRouter(
    prefix=settings.api_prefix.prefix,
)

router.include_router(router=fruit_router)
