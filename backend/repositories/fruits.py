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
from sqlalchemy.exc import DBAPIError
from fastapi import HTTPException


class FruitsRepository:
    model = FruitModel

    async def get_all(self) -> list[FruitModel]:
        async with await database.session_getter() as session:
            result = await session.execute(select(self.model))
        return list(result.scalars().all())
    
    async def get_by_id(self, fruit_id: int) -> FruitModel | None:
        async with await database.session_getter() as session:
            fruit: self.model | None = await session.get(self.model, fruit_id)
        return fruit
    
    async def get_first(self, count: int) -> list[FruitModel]:
        async with await database.session_getter() as session:
            result = await session.execute(select(self.model).limit(count))
        return list(result.scalars().all())

    async def get_by_title(self, title: FruitSearch) -> list[FruitModel]:
        stmt = (
            select(self.model)
            .filter(self.model.title.ilike(f"%{title.fruits_title}%"))
        )
        async with await database.session_getter() as session:
            result = await session.execute(stmt)
        return list(result.scalars().all())
    
    async def create(self, fruit: FruitCreate) -> FruitModel:
        stmt = (
            insert(self.model)
            .values(fruit.model_dump())
            .returning(self.model)
        )
        async with await database.session_getter() as session:
            try:
                result = await session.execute(stmt)
                await session.commit()
            except DBAPIError as exception:
                await session.rollback()
                # Фрукт с таким названием уже существует
                raise HTTPException(status_code=400, detail="A fruit with that title already exists")
        return result.scalars().one()

    async def full_update_by_id(self, fruit: FruitFullUpdateById) -> FruitModel:
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
        async with await database.session_getter() as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.scalar_one_or_none()
    
    async def full_update_by_title(self, fruit: FruitFullUpdateByTitle) -> FruitModel:
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
        async with await database.session_getter() as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.scalar_one_or_none()

    async def partial_update_by_id(self, fruit: FruitPartialUpdateById) -> FruitModel:
        print(fruit.id)
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
        async with await database.session_getter() as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.scalar_one_or_none()
    
    async def partial_update_by_title(self, fruit: FruitPartialUpdateByTitle) -> FruitModel:
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
        async with await database.session_getter() as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.scalar_one_or_none()
    
    async def delete_by_id(self, fruit: FruitDeleteById) -> FruitModel:
        stmt = (
            delete(self.model)
            .where(self.model.id == fruit.id)
            .returning(self.model)
        )
        async with await database.session_getter() as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.scalars().one_or_none()
    
    async def delete_by_title(self, fruit: FruitDeleteByTitle) -> FruitModel:
        stmt = (
            delete(self.model)
            .where(self.model.title == fruit.title)
            .returning(self.model)
        )
        async with await database.session_getter() as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.scalars().one_or_none()
