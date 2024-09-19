from core.cache import cache
from core.config import settings
import orjson


class CacheFruitsRepository:
    async def get_all(self):
        async with cache.redis_cache.client() as redis_client:
            data = await redis_client.get("fruits_all")
            if data:
                return orjson.loads(data)
            else:
                return None

    async def get_by_id(self, id: int):
        async with cache.redis_cache.client() as redis_client:
            data = await redis_client.get(f"fruit_{id}")
            if data:
                return orjson.loads(data)
            else:
                return None

    async def set_all(self, payload: list[dict]):
        async with cache.redis_cache.client() as redis_client:
            await redis_client.set("fruits_all", orjson.dumps(payload), ex=settings.cache.exp_seconds)

    async def set_by_id(self, payload: dict):
        async with cache.redis_cache.client() as redis_client:
            await redis_client.set(f"fruit_{payload.get('id')}", orjson.dumps(payload), ex=settings.cache.exp_seconds)

    async def delete_by_id(self, id: int):
        async with cache.redis_cache.client() as redis_client:
            await redis_client.delete(f"fruit_{id}")
