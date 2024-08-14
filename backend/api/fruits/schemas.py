from fastapi import HTTPException
from pydantic import ConfigDict, BaseModel, field_validator


class FruitBase(BaseModel):
    title: str = ""
    price: int = 0
    description: str | None = ""


class FruitCreate(FruitBase):
    @field_validator("title")
    def check_title(cls, value):
        if not value:
            # Поле "название" является пустым
            raise HTTPException(status_code=400, detail="The <title> field is empty")
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <title> field is incorrect (the maximum length is 64 "
                "characters)",
            )
        return value

    @field_validator("price")
    def check_price(cls, value):
        if value < 0:
            # Поле "цена" должно быть больше или равно нулю
            raise HTTPException(
                status_code=400,
                detail="The <price> field must be greater than or equal to zero",
            )
        return value


class FruitRead(FruitBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class FruitUpdate(BaseModel):
    id: int
    new_title: str = ""
    new_price: int = 0
    new_description: str | None = ""

    @field_validator("new_title")
    def check_title(cls, value):
        if not value:
            # Поле "название" является пустым
            raise HTTPException(
                status_code=400, detail="The <new_title> field is empty"
            )
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <new_title> field is incorrect (the maximum length is 64 "
                "characters)",
            )
        return value

    @field_validator("new_price")
    def check_price(cls, value):
        if value < 0:
            # Поле "цена" должно быть больше или равно нулю
            raise HTTPException(
                status_code=400,
                detail="The <new_price> field must be greater than or equal to zero",
            )
        return value


class FruitDelete(BaseModel):
    id: int
