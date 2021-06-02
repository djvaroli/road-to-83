from typing import *
import os
import datetime
import pytz
import time
from tzlocal import get_localzone
from datetime import datetime as dt
from dateutil import parser
from dotenv import load_dotenv

import elasticsearch_utils
from decorators import add_request_status_info

load_dotenv()

DAILY_CALORIE_NEED = int(os.environ.get("DAILY_CALORIE_NEED", 2000))


@add_request_status_info
def log_metrics_in_es(
        metrics: Dict,
        user_id: str,
        timestamp: int = time.time(),
        index: str = "road83-metric-logs",
        timezone: pytz.timezone = get_localzone(),
        document_id: Optional[str] = None
):
    es = elasticsearch_utils.get_es_client()

    document = {
        **metrics,
        "date": dt.fromtimestamp(timestamp, tz=timezone),
        "user_id": user_id
    }

    if document_id:
        result = es.index(index, body=document, id=document_id)
    else:
        result = es.index(index, body=document)

    return result


@add_request_status_info
def get_calorie_window_stats(
        window_size_days: int = 7,
        index: str = "road83-metric-logs",
        field: str = "calories",
        order: str = "desc"
):
    es = elasticsearch_utils.get_es_client()

    query = {
        "size": 5000,
        "sort": [
            {"date": {"order": order}}
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "exists": {
                            "field": field
                        }
                    },
                    {
                        "range": {
                            "date": {
                                "gte": f"now-{window_size_days}d"
                            }
                        }
                    }
                ]
            }
        }
    }

    hits = es.search(index=index, body=query)['hits']['hits']
    hits = [hit_['_source'] for hit_ in hits]

    result = {
        "history": [],
        "summary": {}
    }

    total_calories_in_window = 0
    unique_dates = set()
    for hit in hits:
        date = parser.parse(hit['date'])
        display_date = date.strftime("%a %B %d")

        # only use the first entry for a specific day in case double texting happened
        # TODO need a better way to handle this case
        if display_date in unique_dates:
            continue
        unique_dates.add(display_date)
        date_calories = hit[field]
        total_calories_in_window += date_calories
        result['history'].append({
            "type": "entry",
            "date": str(date),
            "display_date": display_date,
            field: date_calories
        })

    average_daily_calories = round(total_calories_in_window / len(unique_dates), 2)
    net_difference = DAILY_CALORIE_NEED * len(unique_dates) - total_calories_in_window

    result['summary'] = {
        "total_calories": total_calories_in_window,
        "window_size_days": window_size_days,
        "unique_days_count": len(unique_dates),
        "average_daily_calories": average_daily_calories,
        "average_daily_calorie_need": DAILY_CALORIE_NEED,
        "average_daily_difference": DAILY_CALORIE_NEED - average_daily_calories,
        "net_difference": net_difference
    }

    return result


