import os

import redis
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
    socket_connect_timeout=0.5,
    socket_timeout=0.5,
)

CACHE_TTL_SECONDS = 3600


def cache_get(key: str):
    try:
        return redis_client.get(key)
    except redis.RedisError:
        return None


def cache_set(key: str, value: str):
    try:
        redis_client.set(key, value, ex=CACHE_TTL_SECONDS)
    except redis.RedisError:
        pass