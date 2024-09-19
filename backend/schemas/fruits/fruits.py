from fastapi import HTTPException
from pydantic import ConfigDict, BaseModel, field_validator
from .base import (
    FruitBase,
    FruitFullUpdateBase,
    FruitPartialUpdateBase,
)


class FruitCreate(FruitBase):
    ...


class FruitSearch(BaseModel):
    fruits_title: str

    @field_validator("fruits_title")
    def check_fruits_title(cls, value):
        if not value:
            # Поле "название" является пустым
            raise HTTPException(status_code=400, detail="The <fruits_title> field is empty")
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <fruits_title> field is incorrect (the maximum length is 64 characters)",
            )
        return value


class FruitRead(FruitBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class FruitFullUpdateById(FruitFullUpdateBase):
    id: int

    @field_validator("id")
    def check_id(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="The <id> field is empty")
        try:
            value = int(value)
        except ValueError:
            raise HTTPException(status_code=400, detail="The <id> field should be a integer")
        return value


class FruitFullUpdateByTitle(FruitFullUpdateBase):
    old_title: str

    @field_validator("old_title")
    def check_old_title(cls, value):
        if not value:
            # Поле "название" является пустым
            raise HTTPException(
                status_code=400, detail="The <old_title> field is empty"
            )
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <old_title> field is incorrect (the maximum length is 64 characters)",
            )
        return value


class FruitDeleteById(BaseModel):
    id: int

    @field_validator("id")
    def check_id(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="The <id> field is empty")
        try:
            value = int(value)
        except ValueError:
            raise HTTPException(status_code=400, detail="The <id> field should be a integer")
        return value


class FruitDeleteByTitle(BaseModel):
    title: str

    @field_validator("title")
    def check_title(cls, value):
        if not value:
            # Поле "название" является пустым
            raise HTTPException(status_code=400, detail="The <title> field is empty")
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <title> field is incorrect (the maximum length is 64 characters)",
            )
        return value


class FruitPartialUpdateByTitle(FruitPartialUpdateBase):
    old_title: str

    @field_validator("old_title")
    def check_old_title(cls, value):
        if not value:
            # Поле "название" является пустым
            raise HTTPException(
                status_code=400, detail="The <old_title> field is empty"
            )
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <old_title> field is incorrect (the maximum length is 64 characters)",
            )
        return value


class FruitPartialUpdateById(FruitPartialUpdateBase):
    id: int

    @field_validator("id")
    def check_id(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="The <id> field is empty")
        try:
            value = int(value)
        except ValueError:
            raise HTTPException(status_code=400, detail="The <id> field should be a integer")
        return value
