from repositories.fruits import FruitsRepository
from schemas.fruits.fruits import (
    FruitRead,
    FruitSearch,
    FruitCreate,
    FruitFullUpdateById,
    FruitFullUpdateByTitle,
    FruitPartialUpdateById,
    FruitPartialUpdateByTitle,
    FruitDeleteById,
    FruitDeleteByTitle,
)


class FruitsService:
    def __init__(self, fruits_repo: FruitsRepository):
        self.fruits_repo: FruitsRepository = fruits_repo()

    async def get_all(self) -> list[FruitRead]:
        result = await self.fruits_repo.get_all()
        return result
    
    async def get_by_id(self, id: int) -> FruitRead:
        result = await self.fruits_repo.get_by_id(fruit_id=id)
        return result
    
    async def get_first(self, count: int) -> list[FruitRead]:
        result = await self.fruits_repo.get_first(count=count)
        return result
    
    async def get_by_title(self, title: FruitSearch) -> list[FruitRead]:
        result = await self.fruits_repo.get_by_title(title=title)
        return result
    
    async def create(self, fruit: FruitCreate) -> FruitRead:
        result = await self.fruits_repo.create(fruit=fruit)
        return result
    
    async def full_update_by_id(self, fruit: FruitFullUpdateById) -> FruitRead:
        result = await self.fruits_repo.full_update_by_id(fruit=fruit)
        return result
    
    async def full_update_by_title(self, fruit: FruitFullUpdateByTitle) -> FruitRead:
        result = await self.fruits_repo.full_update_by_title(fruit=fruit)
        return result
    
    async def partial_update_by_id(self, fruit: FruitPartialUpdateById) -> FruitRead:
        result = await self.fruits_repo.partial_update_by_id(fruit=fruit)
        return result
    
    async def partial_update_by_title(self, fruit: FruitPartialUpdateByTitle) -> FruitRead:
        result = await self.fruits_repo.partial_update_by_title(fruit=fruit)
        return result
    
    async def delete_by_id(self, fruit: FruitDeleteById) -> FruitRead:
        result = await self.fruits_repo.delete_by_id(fruit=fruit)
        return result
    
    async def delete_by_title(self, fruit: FruitDeleteByTitle) -> FruitRead:
        result = await self.fruits_repo.delete_by_title(fruit=fruit)
        return result
