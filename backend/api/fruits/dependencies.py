from services.fruits import FruitsService
from repositories.fruits import FruitsRepository


async def fruits_service():
    return FruitsService(FruitsRepository)
