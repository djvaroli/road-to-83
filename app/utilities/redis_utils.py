import os
from typing import *
import logging
from urllib.parse import urlparse

import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = urlparse(os.environ.get("REDIS_URL"))


def get_redis_client():
    return redis.Redis(
        host=REDIS_URL.hostname,
        port=REDIS_URL.port,
        username=REDIS_URL.username,
        password=REDIS_URL.password,
        ssl=True,
        ssl_cert_reqs=None
    )

