from aiogram import types
from aiogram.utils import markdown


async def send_one_fruit(message: types.Message, fruit: dict):
    await message.answer(
        text=f"""{markdown.hbold("Фрукт")} &quot;{fruit.get("title")}&quot;
{markdown.hbold("Цена =")} {fruit.get("price")}
{markdown.hbold("Описание: ")}
{fruit.get("description") if fruit.get("description", False) else "Описание отсутствует"}
""",
    )
