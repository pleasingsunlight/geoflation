import redis
import json

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


def get_cache(key):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cache(key, value, expire=300):
    redis_client.setex(key, expire, json.dumps(value))