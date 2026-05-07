import os
import json
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


def get_cache(key):
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception:
        return None

    return None


def set_cache(key, value, expire=300):
    try:
        redis_client.setex(
            key,
            expire,
            json.dumps(value)
        )
    except Exception:
        pass