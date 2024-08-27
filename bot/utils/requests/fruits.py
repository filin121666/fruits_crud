from aiohttp import ClientSession
from core.settings import settings


async def get_all_fruits():
    async with ClientSession() as session:
        async with session.get(url=f"{settings.api.url}fruits/") as response:
            status = response.status
            data: list[dict] | dict = await response.json()
    return status, data


async def get_first_fruits(count: int):
    async with ClientSession() as session:
        async with session.get(url=f"{settings.api.url}fruits/get_first/", params={"count": count}) as response:
            status = response.status
            data: list[dict] | dict = await response.json()
    return status, data


async def search_fruits_by_title(fruits_title: str):
    async with ClientSession() as session:
        async with session.get(url=f"{settings.api.url}fruits/search/", json={"fruits_title": fruits_title}) as response:
            status = response.status
            data: list[dict] | dict = await response.json()
    return status, data


async def create_fruit(fruit: dict):
    async with ClientSession() as session:
        async with session.post(url=f"{settings.api.url}fruits/", json=fruit) as response:
            status = response.status
            data: dict = await response.json()
    return status, data


async def full_update_fruit_by_title(update_fruit: dict):
    async with ClientSession() as session:
        async with session.put(url=f"{settings.api.url}fruits/by_title/", json=update_fruit) as response:
            status = response.status
            data: dict = await response.json()
    return status, data


async def delete_fruit_by_title(title: str):
    async with ClientSession() as session:
        async with session.delete(url=f"{settings.api.url}fruits/by_title/", json={"title": title}) as response:
            status = response.status
            data: dict = await response.json()
    return status, data


async def partial_update_fruit_by_title(update_fruit: dict):
    async with ClientSession() as session:
        async with session.patch(url=f"{settings.api.url}fruits/by_title/", json=update_fruit) as response:
            status = response.status
            data: dict = await response.json()
    return status, data
