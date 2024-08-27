from fastapi import HTTPException
from sqlalchemy import (
    select,
    insert,
    update,
    delete,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
import asyncpg

from .schemas import (
    FruitCreate,
    FruitFullUpdateById,
    FruitDeleteById,
    FruitSearch,
    FruitFullUpdateByTitle,
    FruitDeleteByTitle,
    FruitPartialUpdateByTitle,
    FruitPartialUpdateById,
)
from core.models import FruitModel


async def get_all_fruits(session: AsyncSession) -> list[FruitModel]:
    result = await session.execute(select(FruitModel))
    result = list(result.scalars().all())
    if result:
        return result
    # Фрукты не найдены
    raise HTTPException(status_code=404, detail="No fruit found")


async def get_fruit_by_id(
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


async def get_first_fruits(
    session: AsyncSession,
    count: int,
) -> list[FruitModel]:
    result = await session.execute(select(FruitModel).limit(count))
    result = list(result.scalars().all())
    if result:
        return result
    # Фрукты не найдены
    raise HTTPException(status_code=404, detail="No fruit found")


async def get_fruits_by_title(
    session: AsyncSession,
    title: FruitSearch,
) -> list[FruitModel]:
    result = await session.execute(select(FruitModel).filter(FruitModel.title.ilike(f"%{title.fruits_title}%")))
    result = list(result.scalars().all())
    if result:
        return result
    # Фрукты не найдены
    raise HTTPException(status_code=404, detail="No fruit found")

async def create_fruit(
    session: AsyncSession,
    fruit_create: FruitCreate,
) -> FruitModel:
    try:
        stmt = (
            insert(FruitModel)
            .values(fruit_create.model_dump())
            .returning(FruitModel)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalars().one()
    except DBAPIError as exception:
        if isinstance(exception.orig, asyncpg.exceptions.UniqueViolationError):
            await session.rollback()
            # Фрукт с таким названием уже существует
            raise HTTPException(status_code=400, detail="A fruit with that title already exists")
        else:
            raise


async def full_update_fruit_by_id(
    session: AsyncSession,
    fruit_update: FruitFullUpdateById,
) -> FruitModel:
    stmt = (
        update(FruitModel)
        .where(FruitModel.id == fruit_update.id)
        .values(
            title=fruit_update.new_title,
            price=fruit_update.new_price,
            description=fruit_update.new_description
        )
        .returning(FruitModel)
    )
    result = await session.execute(stmt)
    updated_fruit = result.scalar_one_or_none()
    
    if not updated_fruit:
        # Не найден, возможно, был введен неверный идентификатор
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect id may have been entered"
        )
    
    await session.commit()
    return updated_fruit


async def full_update_fruit_by_title(
    session: AsyncSession,
    fruit_update: FruitFullUpdateByTitle,
) -> FruitModel:
    stmt = (
        update(FruitModel)
        .where(FruitModel.title == fruit_update.old_title)
        .values(
            title=fruit_update.new_title,
            price=fruit_update.new_price,
            description=fruit_update.new_description
        )
        .returning(FruitModel)
    )
    result = await session.execute(stmt)
    updated_fruit = result.scalar_one_or_none()
    
    if not updated_fruit:
        # Не найдено, возможно, был введен неверный <old_title>.
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect <old_title> may have been entered"
        )
    
    await session.commit()
    return updated_fruit


async def delete_fruit_by_id(
    session: AsyncSession,
    fruit_delete: FruitDeleteById,
) -> FruitModel:
    stmt = (
        delete(FruitModel)
        .where(FruitModel.id == fruit_delete.id)
        .returning(FruitModel)
    )
    result = await session.execute(stmt)
    deleted_fruit = result.scalars().one_or_none()
    
    if not deleted_fruit:
        # Не найден, возможно, был введен неверный идентификатор
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect id may have been entered"
        )
    
    await session.commit()
    return deleted_fruit


async def delete_fruit_by_title(
    session: AsyncSession,
    fruit_delete: FruitDeleteByTitle,
) -> FruitModel:
    stmt = (
        delete(FruitModel)
        .where(FruitModel.title == fruit_delete.title)
        .returning(FruitModel)
    )
    result = await session.execute(stmt)
    deleted_fruit = result.scalars().one_or_none()
    
    if not deleted_fruit:
        # Не найдено, возможно, было введено неверное название
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect title may have been entered"
        )
    
    await session.commit()
    return deleted_fruit


async def partial_update_fruit_by_title(
    session: AsyncSession,
    fruit_update: FruitPartialUpdateByTitle,
) -> FruitModel:
    stmt = (
        update(FruitModel)
        .where(FruitModel.title == fruit_update.old_title)
        .values(
            title=fruit_update.new_title if fruit_update.new_title is not False else FruitModel.title,
            price=fruit_update.new_price if fruit_update.new_price is not False else FruitModel.price,
            description=fruit_update.new_description if fruit_update.new_description is not False else FruitModel.description,
        )
        .returning(FruitModel)
    )
    result = await session.execute(stmt)
    updated_fruit = result.scalar_one_or_none()

    if not updated_fruit:
        # Не найдено, возможно, был введен неверный <old_title>.
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect <old_title> may have been entered"
        )

    await session.commit()
    return updated_fruit


async def partial_update_fruit_by_id(
    session: AsyncSession,
    fruit_update: FruitPartialUpdateById,
) -> FruitModel:
    stmt = (
        update(FruitModel)
        .where(FruitModel.id == fruit_update.id)
        .values(
            title=fruit_update.new_title if fruit_update.new_title is not False else FruitModel.title,
            price=fruit_update.new_price if fruit_update.new_price is not False else FruitModel.price,
            description=fruit_update.new_description if fruit_update.new_description is not False else FruitModel.description,
        )
        .returning(FruitModel)
    )
    result = await session.execute(stmt)
    updated_fruit = result.scalar_one_or_none()

    if not updated_fruit:
        # Не найден, возможно, был введен неверный идентификатор
        raise HTTPException(
            status_code=404, detail="Not found, an incorrect id may have been entered"
        )

    await session.commit()
    return updated_fruit
