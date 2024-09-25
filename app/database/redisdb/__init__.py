from flask_redis import Redis

from app.database.redisdb.services import RedisHandler


rediska: Redis = Redis()

__all__ = [
    "rediska",
    "RedisHandler"
]
