from utils.repository import SQLAlchemyRepository
from models.fruits import FruitModel
from core.database import database
from sqlalchemy import (
    select,
    insert,
    update,
    delete,
)
from schemas.fruits.fruits import (
    FruitSearch,
    FruitCreate,
    FruitFullUpdateById,
    FruitFullUpdateByTitle,
    FruitPartialUpdateById,
    FruitPartialUpdateByTitle,
    FruitDeleteById,
    FruitDeleteByTitle,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
import asyncpg
from fastapi import HTTPException


class FruitsRepository(SQLAlchemyRepository):
    model = FruitModel

    async def get_all(self) -> list[FruitModel]:
        session: AsyncSession = await database.session_getter()
        result = await session.execute(select(self.model))
        result = list(result.scalars().all())
        if result:
            return result
        raise HTTPException(
            status_code=404, detail="No fruit found"
        )
    
    async def get_by_id(self, fruit_id: int) -> FruitModel | None:
        session: AsyncSession = await database.session_getter()
        fruit: self.model | None = await session.get(self.model, fruit_id)
        if fruit is None:
            # Не найдено, возможно был введён некорректный id
            raise HTTPException(
                status_code=404, detail="Not found, an incorrect id may have been entered"
            )
        return fruit
    
    async def get_first(self, count: int) -> list[FruitModel]:
        session: AsyncSession = await database.session_getter()
        result = await session.execute(select(self.model).limit(count))
        result = list(result.scalars().all())
        if result:
            return result
        # Фрукты не найдены
        raise HTTPException(status_code=404, detail="No fruit found")

    async def get_by_title(self, title: FruitSearch) -> list[FruitModel]:
        session: AsyncSession = await database.session_getter()
        result = await session.execute(select(self.model).filter(self.model.title.ilike(f"%{title.fruits_title}%")))
        result = list(result.scalars().all())
        if result:
            return result
        # Фрукты не найдены
        raise HTTPException(status_code=404, detail="No fruit found")
    
    async def create(self, fruit: FruitCreate) -> FruitModel:
        session: AsyncSession = await database.session_getter()
        try:
            stmt = (
                insert(self.model)
                .values(fruit.model_dump())
                .returning(self.model)
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

    async def full_update_by_id(self, fruit: FruitFullUpdateById) -> FruitModel:
        session: AsyncSession = await database.session_getter()
        stmt = (
            update(self.model)
            .where(self.model.id == fruit.id)
            .values(
                title=fruit.new_title,
                price=fruit.new_price,
                description=fruit.new_description
            )
            .returning(self.model)
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
    
    async def full_update_by_title(self, fruit: FruitFullUpdateByTitle) -> FruitModel:
        session: AsyncSession = await database.session_getter()
        stmt = (
            update(self.model)
            .where(self.model.title == fruit.old_title)
            .values(
                title=fruit.new_title,
                price=fruit.new_price,
                description=fruit.new_description
            )
            .returning(self.model)
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

    async def partial_update_by_id(self, fruit: FruitPartialUpdateById) -> FruitModel:
        session: AsyncSession = await database.session_getter()
        stmt = (
            update(self.model)
            .where(self.model.id == fruit.id)
            .values(
                title=fruit.new_title if fruit.new_title is not False else self.model.title,
                price=fruit.new_price if fruit.new_price is not False else self.model.price,
                description=fruit.new_description if fruit.new_description is not False else self.model.description,
            )
            .returning(self.model)
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
    
    async def partial_update_by_title(self, fruit: FruitPartialUpdateByTitle) -> FruitModel:
        session: AsyncSession = await database.session_getter()
        stmt = (
            update(self.model)
            .where(self.model.title == fruit.old_title)
            .values(
                title=fruit.new_title if fruit.new_title is not False else self.model.title,
                price=fruit.new_price if fruit.new_price is not False else self.model.price,
                description=fruit.new_description if fruit.new_description is not False else self.model.description,
            )
            .returning(self.model)
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
    
    async def delete_by_id(self, fruit: FruitDeleteById) -> FruitModel:
        session: AsyncSession = await database.session_getter()
        stmt = (
            delete(self.model)
            .where(self.model.id == fruit.id)
            .returning(self.model)
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
    
    async def delete_by_title(self, fruit: FruitDeleteByTitle) -> FruitModel:
        session: AsyncSession = await database.session_getter()
        stmt = (
            delete(self.model)
            .where(self.model.title == fruit.title)
            .returning(self.model)
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
