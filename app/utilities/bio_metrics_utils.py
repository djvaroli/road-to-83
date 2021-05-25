from typing import *
import datetime
import time
from datetime import datetime as dt

from app.utilities.redis_utils import get_redis_client
from app.utilities import elasticsearch_utils
from app.utilities.decorators import add_request_status_info


@add_request_status_info
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

    return es.index(index=index, body=document)
