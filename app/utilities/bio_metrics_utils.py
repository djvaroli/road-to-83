from typing import *
import datetime
import time
from datetime import datetime as dt

from app.utilities.redis_utils import get_redis_client
from app.utilities import elasticsearch_utils
from app.utilities.decorators import request_status


@request_status
def log_metrics_in_redis(
        weight: float,
        timestamp: int = int(time.time()),
        key: str = "road83::weight"
):
    redis = get_redis_client()
    to_add = {timestamp: weight}
    return redis.zadd(key, to_add)


@request_status
def log_metrics_in_es(
        metrics: Dict,
        user_id: str,
        timestamp: int = time.time(),
        index: str = "road83-metric-logs"
):
    es = elasticsearch_utils.get_es_client()
    document = {
        **metrics,
        "date": dt.fromtimestamp(timestamp, tz=None),
        "user_id": user_id
    }

    print(document)
    return 1
    # result = es.index(index=index, body=document)
