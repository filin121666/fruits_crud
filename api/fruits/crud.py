from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import FruitCreate, FruitUpdate, FruitDelete
from core.models import FruitModel


async def get_all_fruits(session: AsyncSession) -> list[FruitModel]:
    query = select(FruitModel)
    result = await session.scalars(query)
    result = list(result.all())
    if result:
        return result
    # Фрукты не найдены
    raise HTTPException(status_code=404, detail="No fruit found")


async def get_one_fruit(
    session: AsyncSession,
    fruit_id: int,
) -> FruitModel:
    fruit: FruitModel | None = await session.get(FruitModel, fruit_id)
    if fruit is None:
        # Не найдено, возможно был введён некорректный id
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect id may have been entered"
        )
    return fruit


async def create_fruit(
    session: AsyncSession,
    fruit_create: FruitCreate,
) -> FruitModel:
    fruit = FruitModel(**fruit_create.model_dump())
    session.add(fruit)
    await session.commit()
    return fruit


async def update_fruit(
    session: AsyncSession,
    fruit_update: FruitUpdate,
) -> FruitModel:
    fruit: FruitModel | None = await session.get(FruitModel, fruit_update.id)
    if fruit is None:
        # Не найдено, возможно был введён некорректный id
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect id may have been entered"
        )
    fruit.title = fruit_update.new_title
    fruit.price = fruit_update.new_price
    fruit.description = fruit_update.new_description
    session.add(fruit)
    await session.commit()
    return fruit


async def delete_fruit(
    session: AsyncSession,
    fruit_delete: FruitDelete,
) -> FruitModel:
    fruit: FruitModel | None = await session.get(FruitModel, fruit_delete.id)
    if fruit is None:
        # Не найдено, возможно был введён некорректный id
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect id may have been entered"
        )
    await session.delete(fruit)
    await session.commit()
    return fruit
