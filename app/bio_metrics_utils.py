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

DAILY_CALORIE_NEED = int(os.environ.get("DAILY_CALORIE_NEED", 2300))
MAINTENANCE_CALORIES = int(os.environ.get("MAINTENANCE_CALORIES", 2700))


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
        window_size_days: int = 14,
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

    documents = es.search(index=index, body=query)['hits']['hits']

    result = {
        "history": [],
        "summary": {}
    }

    total_calories_in_window = 0
    unique_dates = set()
    for doc in documents:
        hit = doc['_source']
        date = parser.parse(hit['date'])
        display_date = date.strftime("%d %B %Y")

        # only use the first entry for a specific day in case double texting happened
        # TODO need a better way to handle this case
        if display_date in unique_dates:
            continue
        unique_dates.add(display_date)
        date_calories = hit[field]
        total_calories_in_window += int(date_calories)
        result['history'].append({
            "type": "entry",
            "id": doc['_id'],
            "date": str(date),
            "display_date": display_date,
            field: date_calories
        })

    average_daily_calories = int(total_calories_in_window / len(unique_dates))
    net_difference = DAILY_CALORIE_NEED * len(unique_dates) - total_calories_in_window
    net_deficit = MAINTENANCE_CALORIES * len(unique_dates) - total_calories_in_window

    result['summary'] = {
        "total_calories": total_calories_in_window,
        "window_size_days": window_size_days,
        "unique_days_count": len(unique_dates),
        "average_daily_calories": average_daily_calories,
        "average_daily_calorie_need": DAILY_CALORIE_NEED,
        "average_daily_difference": DAILY_CALORIE_NEED - average_daily_calories,
        "net_difference": net_difference,
        "average_daily_maintenance_calories": MAINTENANCE_CALORIES,
        "average_daily_caloric_deficit": MAINTENANCE_CALORIES - average_daily_calories,
        "net_calorie_deficit": net_deficit
    }

    return result


def get_weight_history(
        window_size: int = 30,
        index: str = "road83-metric-logs",
        field: str = "weight",
        order: str = "asc",
        sort_field: str = "date"
) -> Dict:
    es = elasticsearch_utils.get_es_client()
    query = {
        "size": 5000,
        "sort": {
            sort_field: {"order": order}
        },
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
                                "gte": f"now-{window_size}d"
                            }
                        }
                    }
                ]
            }
        }
    }

    documents = es.search(body=query, index=index)['hits']['hits']

    result = {
        "history": [],
        "summary": {}
    }
    for doc in documents:
        doc_id = doc["_id"]
        source = doc["_source"]

        result['history'].append({
            "weight": source[field],
            "date": parser.parse(source["date"]),
            "display_date": parser.parse(source["date"]).strftime("%d %B %Y @ %I %p"),
            "id": doc_id
        })

    # hardcode for now, no need to overcomplicate things yet
    result['summary'] = {
        "target_weight": 83.0,
        "start_weight": 97.0,
        "step1": 87.0,
        "step2": 85.0
    }

    return result
