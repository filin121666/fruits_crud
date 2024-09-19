from services.fruits import FruitsService
from repositories.fruits import FruitsRepository
from repositories.cache import CacheFruitsRepository


async def fruits_service():
    return FruitsService(
        FruitsRepository,
        CacheFruitsRepository,
    )
