from config.db import get_redis
from redis.asyncio import Redis


class RedisService:

    def __init__(self):
        self.redis = None

    async def _init_redis(self):
        if not self.redis:
            self.redis: Redis = await get_redis()

    async def set(self, key: str, value: str):
        await self._init_redis()
        await self.redis.set(key, value)

    async def get(self, key: str):
        await self._init_redis()
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self._init_redis()
        await self.redis.delete(key)
