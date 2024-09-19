from typing import Annotated
from fastapi import APIRouter, Depends

from schemas.fruits.fruits import (
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
from services.fruits import FruitsService
from .dependencies import fruits_service


router = APIRouter(
    prefix=settings.api.prefix.fruits_prefix,
    tags=["Fruits"],
)


@router.get("/", response_model=list[FruitRead], status_code=200)
async def get_all_fruits(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
):
    return await fruits_service.get_all()


@router.get("/get_first/", response_model=list[FruitRead], status_code=200)
async def get_first_fruits(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    count: int,
):
    return await fruits_service.get_first(count=count)


@router.get("/{fruit_id:int}/", response_model=FruitRead, status_code=200)
async def get_fruit_by_id(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruit_id: int,
):
    return await fruits_service.get_by_id(id=fruit_id)


@router.get("/search/", response_model=list[FruitRead], status_code=200)
async def get_fruits_by_title(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruits_title: FruitSearch,
):
    return await fruits_service.get_by_title(title=fruits_title)


@router.post("/", response_model=FruitRead, status_code=201)
async def create_fruit(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruit_create: FruitCreate,
):
    return await fruits_service.create(fruit=fruit_create)


@router.put("/", response_model=FruitRead, status_code=200)
async def full_update_fruit_by_id(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruit_update: FruitFullUpdateById,
):
    return await fruits_service.full_update_by_id(fruit=fruit_update)


@router.delete("/", response_model=FruitRead, status_code=200)
async def delete_fruit_by_id(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruit_delete: FruitDeleteById,
):
    return await fruits_service.delete_by_id(fruit=fruit_delete)


@router.put("/by_title/", response_model=FruitRead, status_code=200)
async def full_update_fruit_by_title(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruit_update: FruitFullUpdateByTitle,
):
    return await fruits_service.full_update_by_title(fruit=fruit_update)


@router.delete("/by_title/", response_model=FruitRead, status_code=200)
async def delete_fruit_by_title(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruit_delete: FruitDeleteByTitle,
):
    return await fruits_service.delete_by_title(fruit=fruit_delete)


@router.patch("/by_title/", response_model=FruitRead, status_code=200)
async def partial_update_by_title(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruit_update: FruitPartialUpdateByTitle,
):
    return await fruits_service.partial_update_by_title(fruit=fruit_update)


@router.patch("/", response_model=FruitRead, status_code=200)
async def partial_update_by_id(
    fruits_service: Annotated[
        FruitsService,
        Depends(fruits_service)
    ],
    fruit_update: FruitPartialUpdateById,
):
    return await fruits_service.partial_update_by_id(fruit=fruit_update)
