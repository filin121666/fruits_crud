from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud as fruits_crud
from .schemas import FruitRead, FruitCreate, FruitDelete, FruitUpdate
from core.config import settings
from core.database import database

router = APIRouter(
    prefix=settings.api_prefix.fruits_prefix,
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


@router.get("/{fruit_id}/", response_model=FruitRead, status_code=200)
async def get_one_fruit(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_id: int,
):
    fruit = await fruits_crud.get_one_fruit(session=session, fruit_id=fruit_id)
    return fruit


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
async def update_fruit(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_update: FruitUpdate,
):
    fruit = await fruits_crud.update_fruit(session=session, fruit_update=fruit_update)
    return fruit


@router.delete("/", response_model=FruitRead, status_code=200)
async def delete_fruit(
    session: Annotated[
        AsyncSession,
        Depends(database.session_getter),
    ],
    fruit_delete: FruitDelete,
):
    fruit = await fruits_crud.delete_fruit(session=session, fruit_delete=fruit_delete)
    return fruit
