from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud as fruits_crud
from .schemas import (
    FruitRead,
    FruitCreate,
    FruitDeleteById,
    FruitFullUpdateById,
    FruitSearch,
    FruitFullUpdateByTitle,
    FruitDeleteByTitle,
    FruitPartialUpdateByTitle,
    FruitPartialUpdateById,
)
from core.config import settings
from core.database import database

router = APIRouter(
    prefix=settings.api.prefix.fruits_prefix,
    tags=["Fruits"],
)


@router.get("/", response_model=list[FruitRead], status_code=200)
async def get_all_fruits(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ]
):
    fruits = await fruits_crud.get_all_fruits(session=session)
    return fruits


@router.get("/get_first/", response_model=list[FruitRead], status_code=200)
async def get_first_fruits(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    count: int,
):
    fruits = await fruits_crud.get_first_fruits(session=session, count=count)
    return fruits


@router.get("/{fruit_id:int}/", response_model=FruitRead, status_code=200)
async def get_fruit_by_id(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_id: int,
):
    fruit = await fruits_crud.get_fruit_by_id(session=session, fruit_id=fruit_id)
    return fruit


@router.get("/search/", response_model=list[FruitRead], status_code=200)
async def get_fruits_by_title(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruits_title: FruitSearch,
):
    fruits = await fruits_crud.get_fruits_by_title(session=session, title=fruits_title)
    return fruits


@router.post("/", response_model=FruitRead, status_code=201)
async def create_fruit(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_create: FruitCreate,
):
    fruit = await fruits_crud.create_fruit(session=session, fruit_create=fruit_create)
    return fruit


@router.put("/", response_model=FruitRead, status_code=200)
async def full_update_fruit_by_id(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_update: FruitFullUpdateById,
):
    fruit = await fruits_crud.full_update_fruit_by_id(session=session, fruit_update=fruit_update)
    return fruit


@router.delete("/", response_model=FruitRead, status_code=200)
async def delete_fruit_by_id(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_delete: FruitDeleteById,
):
    fruit = await fruits_crud.delete_fruit_by_id(session=session, fruit_delete=fruit_delete)
    return fruit


@router.put("/by_title/", response_model=FruitRead, status_code=200)
async def full_update_fruit_by_title(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_update: FruitFullUpdateByTitle,
):
    fruit = await fruits_crud.full_update_fruit_by_title(session=session, fruit_update=fruit_update)
    return fruit


@router.delete("/by_title/", response_model=FruitRead, status_code=200)
async def delete_fruit_by_title(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_delete: FruitDeleteByTitle,
):
    fruit = await fruits_crud.delete_fruit_by_title(session=session, fruit_delete=fruit_delete)
    return fruit


@router.patch("/by_title/", response_model=FruitRead, status_code=200)
async def partial_update_by_title(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_update: FruitPartialUpdateByTitle,
):
    fruit = await fruits_crud.partial_update_fruit_by_title(session=session, fruit_update=fruit_update)
    return fruit


@router.patch("/", response_model=FruitRead, status_code=200)
async def partial_update_by_id(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_update: FruitPartialUpdateById,
):
    fruit = await fruits_crud.partial_update_fruit_by_id(session=session, fruit_update=fruit_update)
    return fruit
