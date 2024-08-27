from fastapi import HTTPException
from pydantic import ConfigDict, BaseModel, field_validator


# class FruitBase(BaseModel):
    # title: str
    # price: int
    # description: str | None


class FruitCreate(BaseModel):
    title: str
    price: int
    description: str | None

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

    @field_validator("price")
    def check_price(cls, value):
        if value < 0:
            # Поле "цена" должно быть больше или равно нулю
            raise HTTPException(
                status_code=400,
                detail="The <price> field must be greater than or equal to zero",
            )
        return value
    
    @field_validator("description")
    def check_description(cls, value):
        return value or None


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


class FruitRead(BaseModel):
    id: int
    title: str
    price: int
    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class FruitFullUpdateById(BaseModel):
    id: int
    new_title: str
    new_price: int
    new_description: str | None

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
                detail="The <new_title> field is incorrect (the maximum length is 64 characters)",
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


class FruitFullUpdateByTitle(BaseModel):
    old_title: str
    new_title: str
    new_price: int
    new_description: str | None

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

    @field_validator("new_title")
    def check_new_title(cls, value):
        if not value:
            # Поле "название" является пустым
            raise HTTPException(
                status_code=400, detail="The <new_title> field is empty"
            )
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <new_title> field is incorrect (the maximum length is 64 characters)",
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


class FruitDeleteById(BaseModel):
    id: int


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


class FruitPartialUpdateByTitle(BaseModel):
    old_title: str
    new_title: str | bool
    new_price: int | bool
    new_description: str | bool | None

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

    @field_validator("new_title")
    def check_new_title(cls, value):
        if isinstance(value, bool):
            if value is False:
                return value
            elif value is True:
                # Если вам нужно, чтобы <new_title> оставался неизменным, значение должно быть false, а не true
                raise HTTPException(
                    status_code=400, detail="If you need the <new_title> to remain the same, the value should be false, not true"
                )
        elif not value:
            # Поле "название" является пустым
            raise HTTPException(
                status_code=400, detail="The <new_title> field is empty"
            )
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <new_title> field is incorrect (the maximum length is 64 characters)",
            )
        return value

    @field_validator("new_price")
    def check_price(cls, value):
        if isinstance(value, bool):
            if value is False:
                return value
            elif value is True:
                # Если вам нужно, чтобы значение <new_price> оставалось неизменным, оно должно быть false, а не true
                raise HTTPException(
                    status_code=400, detail="If you need the <new_price> to remain the same, the value should be false, not true"
                )
        elif value < 0:
            # Поле "цена" должно быть больше или равно нулю
            raise HTTPException(
                status_code=400,
                detail="The <new_price> field must be greater than or equal to zero",
            )
        return value
    
    @field_validator("new_description")
    def check_new_description(cls, value):
        if isinstance(value, bool):
            if value is False:
                return value
            elif value is True:
                # Если вам нужно, чтобы <new_description> оставалось неизменным, значение должно быть false, а не true
                raise HTTPException(
                    status_code=400, detail="If you need the <new_description> to remain the same, the value should be false, not true"
                )
        return value


class FruitPartialUpdateById(BaseModel):
    id: int
    new_title: str | bool
    new_price: int | bool
    new_description: str | bool | None

    @field_validator("new_title")
    def check_new_title(cls, value):
        if isinstance(value, bool):
            if value is False:
                return value
            elif value is True:
                # Если вам нужно, чтобы <new_title> оставался прежним, значение должно быть false, а не true
                raise HTTPException(
                    status_code=400, detail="If you need the <new_title> to remain the same, the value should be false, not true"
                )
        elif not value:
            # Поле "название" является пустым
            raise HTTPException(
                status_code=400, detail="The <new_title> field is empty"
            )
        elif len(value) > 64:
            # Поле "название" неккоректно (максимальная длина - 64 символа)
            raise HTTPException(
                status_code=400,
                detail="The <new_title> field is incorrect (the maximum length is 64 characters)",
            )
        return value

    @field_validator("new_price")
    def check_price(cls, value):
        if isinstance(value, bool):
            if value is False:
                return value
            elif value is True:
                # Если вам нужно, чтобы значение <new_price> оставалось неизменным, оно должно быть false, а не true
                raise HTTPException(
                    status_code=400, detail="If you need the <new_price> to remain the same, the value should be false, not true"
                )
        elif value < 0:
            # Поле "цена" должно быть больше или равно нулю
            raise HTTPException(
                status_code=400,
                detail="The <new_price> field must be greater than or equal to zero",
            )
        return value
    
    @field_validator("new_description")
    def check_new_description(cls, value):
        if isinstance(value, bool):
            if value is False:
                return value
            elif value is True:
                # Если вам нужно, чтобы <new_description> оставалось неизменным, значение должно быть false, а не true
                raise HTTPException(
                    status_code=400, detail="If you need the <new_description> to remain the same, the value should be false, not true"
                )
        return value
