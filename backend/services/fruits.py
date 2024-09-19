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
from fastapi import HTTPException
from repositories.cache import CacheFruitsRepository


class FruitsService:
    def __init__(
            self,
            fruits_repo: FruitsRepository,
            cache_repo: CacheFruitsRepository,
        ):
        self.fruits_repo: FruitsRepository = fruits_repo()
        self.cache_repo: CacheFruitsRepository = cache_repo()

    async def get_all(self) -> list[FruitRead]:
        if data := await self.cache_repo.get_all():
            return data
        result = await self.fruits_repo.get_all()
        if result:
            payload: list[dict] = [FruitRead(**i.__dict__).model_dump() for i in result]
            await self.cache_repo.set_all(payload=payload)
        else:
            raise HTTPException(
                status_code=404, detail="No fruit found"
            )
        return result
    
    async def get_by_id(self, id: int) -> FruitRead:
        if data := await self.cache_repo.get_by_id(id=id):
            return data
        result = await self.fruits_repo.get_by_id(fruit_id=id)
        if result is None:
            # Не найдено, возможно был введён некорректный id
            raise HTTPException(
                status_code=404, detail="Not found, an incorrect id may have been entered"
            )
        payload = FruitRead(**result.__dict__).model_dump()
        await self.cache_repo.set_by_id(payload=payload)
        return result
    
    async def get_first(self, count: int) -> list[FruitRead]:
        result = await self.fruits_repo.get_first(count=count)
        if result:
            return result
        # Фрукты не найдены
        raise HTTPException(status_code=404, detail="No fruit found")
    
    async def get_by_title(self, title: FruitSearch) -> list[FruitRead]:
        result = await self.fruits_repo.get_by_title(title=title)
        if result:
            return result
        # Фрукты не найдены
        raise HTTPException(status_code=404, detail="No fruit found")
    
    async def create(self, fruit: FruitCreate) -> FruitRead:
        result = await self.fruits_repo.create(fruit=fruit)
        payload = FruitRead(**result.__dict__).model_dump()
        await self.cache_repo.set_by_id(payload=payload)
        return result
    
    async def full_update_by_id(self, fruit: FruitFullUpdateById) -> FruitRead:
        result = await self.fruits_repo.full_update_by_id(fruit=fruit)
        if not result:
            # Не найден, возможно, был введен неверный идентификатор
            raise HTTPException(
                status_code=404, detail="Not found, an incorrect id may have been entered"
            )
        payload = FruitRead(**result.__dict__).model_dump()
        await self.cache_repo.set_by_id(payload=payload)
        return result
    
    async def full_update_by_title(self, fruit: FruitFullUpdateByTitle) -> FruitRead:
        result = await self.fruits_repo.full_update_by_title(fruit=fruit)
        if not result:
            # Не найдено, возможно, был введен неверный <old_title>.
            raise HTTPException(
                status_code=404, detail="Not found, an incorrect <old_title> may have been entered"
            )
        payload = FruitRead(**result.__dict__).model_dump()
        await self.cache_repo.set_by_id(payload=payload)
        return result
    
    async def partial_update_by_id(self, fruit: FruitPartialUpdateById) -> FruitRead:
        result = await self.fruits_repo.partial_update_by_id(fruit=fruit)
        if not result:
            # Не найден, возможно, был введен неверный идентификатор
            raise HTTPException(
                status_code=404, detail="Not found, an incorrect id may have been entered"
            )
        payload = FruitRead(**result.__dict__).model_dump()
        await self.cache_repo.set_by_id(payload=payload)
        return result
    
    async def partial_update_by_title(self, fruit: FruitPartialUpdateByTitle) -> FruitRead:
        result = await self.fruits_repo.partial_update_by_title(fruit=fruit)
        if not result:
            # Не найдено, возможно, был введен неверный <old_title>.
            raise HTTPException(
                status_code=404, detail="Not found, an incorrect <old_title> may have been entered"
            )
        payload = FruitRead(**result.__dict__).model_dump()
        await self.cache_repo.set_by_id(payload=payload)
        return result
    
    async def delete_by_id(self, fruit: FruitDeleteById) -> FruitRead:
        result = await self.fruits_repo.delete_by_id(fruit=fruit)
        if not result:
            # Не найден, возможно, был введен неверный идентификатор
            raise HTTPException(
                status_code=404, detail="Not found, an incorrect id may have been entered"
            )
        await self.cache_repo.delete_by_id(id=result.id)
        return result
    
    async def delete_by_title(self, fruit: FruitDeleteByTitle) -> FruitRead:
        result = await self.fruits_repo.delete_by_title(fruit=fruit)
        if not result:
            # Не найдено, возможно, было введено неверное название
            raise HTTPException(
                status_code=404, detail="Not found, an incorrect title may have been entered"
            )
        await self.cache_repo.delete_by_id(id=result.id)
        return result
