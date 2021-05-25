

from app.utilities.redis_utils import get_redis_client


def get_user_auth_level(
        phone_number: str,
        key: str = "road83::user-auth-level"
) -> int:
    redis = get_redis_client()
    user_auth_level = 0
    if redis.hexists(key, phone_number):
        user_auth_level = int(redis.hget(key, phone_number).decode())

    return user_auth_level

