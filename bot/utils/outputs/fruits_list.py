from aiogram import types
from aiogram.utils import markdown


async def send_fruits_list(message: types.Message, fruits_list: list[dict]):
    for i in fruits_list:
        await message.answer(
            text=f"""{markdown.hbold("Фрукт")} &quot;{i.get("title")}&quot;
{markdown.hbold("Цена =")} {i.get("price")}
{markdown.hbold("Описание: ")}
{i.get("description") if i.get("description", False) else "Описание отсутствует"}
""",
        )


async def send_fruits_list_with_numeration(message: types.Message, fruits_list: list[dict]):
    for i in range(len(fruits_list)):
        await message.answer(
            text=f"""{i+1}:
{markdown.hbold("Фрукт")} &quot;{fruits_list[i].get("title")}&quot;
{markdown.hbold("Цена =")} {fruits_list[i].get("price")}
{markdown.hbold("Описание: ")}
{fruits_list[i].get("description") if fruits_list[i].get("description", False) else "Описание отсутствует"}
""",
        )
