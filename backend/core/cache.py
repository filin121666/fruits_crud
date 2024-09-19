from redis.asyncio import (
    from_url,
    Redis
)
from core.config import settings


class Cache:
    def __init__(
        self,
        url: str,
    ) -> None:
        self.url = url
        self.redis_cache: Redis = from_url(
            url=url,
            encoding="utf-8",
            decode_responses=True,
        )


cache = Cache(
    settings.cache.get_url,
)
