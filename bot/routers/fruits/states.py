from aiogram.fsm.state import StatesGroup, State


class GetFirstFruitsForm(StatesGroup):
    count = State()


class SearchFruits(StatesGroup):
    fruits_title = State()


class CreateFruitForm(StatesGroup):
    title = State()
    price = State()
    description_choice = State()
    description = State()


class FullUpdateFruitForm(StatesGroup):
    old_title = State()
    new_title = State()
    new_price = State()
    new_description_choice = State()
    new_description = State()


class DeleteFruitForm(StatesGroup):
    title = State()


class PartialUpdateFruitForm(StatesGroup):
    old_title = State()
    new_title_update_choice = State()
    new_title = State()
    new_price_update_choice = State()
    new_price = State()
    new_description_update_choice = State()
    new_description_choice = State()
    new_description = State()
