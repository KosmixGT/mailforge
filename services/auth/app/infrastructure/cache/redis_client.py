import json
from redis import Redis
from mailforge_shared.core.config.settings import settings

redis_client = Redis(
    host='redis',
    port=6379,
    decode_responses=True
)

class RedisCache:
    @staticmethod
    async def get_user(user_id: int):
        data = redis_client.get(f"user:{user_id}")
        return json.loads(data) if data else None

    @staticmethod
    async def set_user(user_id: int, user_data: dict):
        redis_client.setex(
            f"user:{user_id}",
            300,  # Cache for 5 minutes
            json.dumps(user_data)
        )
