import time

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse

from apex_charts_utils import line_series_dict
from elasticsearch_utils import delete_document_by_id, update_document_by_id
from messaging_utils import get_pipeline_for_sms_command
from bio_metrics_utils import get_calorie_window_stats, log_metrics_in_es, get_weight_history
from decorators import validate_user_auth_level, messaging_response
from pydantic_models import DeleteEntry, EditEntry, ResponseContent, NewEntry

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
@app.get("/home")
def home():
    """
    The home page of the app. May the force be with you!
    :return:
    """
    return "Hello there!"


@app.post("/interact/sms", status_code=200)
@validate_user_auth_level(level=5, field="From")
def interact_sms(
        From: str =  Form(default=None),
        Body: str = Form(default=None),
        timestamp: int = int(time.time())
):
    """
    API endpoint for all sms interactions using Twilio
    :param From:
    :param Body:
    :param timestamp:
    :return:
    """

    pipeline = get_pipeline_for_sms_command(Body)
    message: MessagingResponse = pipeline(Body, From, timestamp)
    return message


@app.get("/history/window_calories")
def get_calorie_stats_in_window(
        windowSizeDays: int = 7
):
    stats = get_calorie_window_stats(window_size_days=windowSizeDays, order="asc")
    summary = stats.data['summary']
    history = stats.data['history']
    maintenance_calories = summary['average_daily_maintenance_calories']
    goal_calories = summary['average_daily_calorie_need']
    daily_average_calories = summary['average_daily_calories']

    series = [
        {
            "name": "Daily Calories",
            "type": "column",
            "data": [entry['calories'] for entry in history]
        },
        {
            "name": "Daily Average Calories",
            "type": "line",
            "data": [daily_average_calories for _ in range(len(history))]
        },
        {
            "name": "Goal Calories",
            "type": "line",
            "data": [goal_calories for _ in range(len(history))]
        },
        {
            "name": "Maintenance Calories",
            "type": "line",
            "data": [maintenance_calories for _ in range(len(history))]
        }
    ]
    stats.data['plot'] = {
        "series": series,
        "chartOptions": {
            "chart": {
                "height": 350,
                "type": "line"
            },
            "stroke": {
                "width": [1, 3, 3, 3],
                "dashArray": [0, 5, 5, 5],
            },
            "title": {
                "text": f'Calorie Consumption (last {windowSizeDays} days)'
            },
            "dataLabels": {
                "enabled": True,
                "enabledOnSeries": []
            },
            "labels": [entry['display_date'] for entry in history],
            "xaxis": {
                "type": "datetime"
            },
            "yaxis": [
                {
                    "title": {
                        "text": "Calorie Intake"
                    }
                }
            ]
        }
    }
    return stats


@app.get("/history/weight")
def get_weight_history_endpoint(
        windowSizeDays: int = 30
):
    # this is not the best way, however this is sufficient to verify the feature design
    weight_data = get_weight_history(window_size=windowSizeDays)
    weight_summary = weight_data['summary']
    weight_history = weight_data['history']

    start_weight = weight_summary['start_weight']
    step1_weight = weight_summary['step1']
    step2_weight = weight_summary['step2']
    target_weight = weight_summary['target_weight']

    series = [
        line_series_dict("Current weight", [entry['weight'] for entry in weight_history]),
        line_series_dict("Starting weight", [start_weight for _ in range(len(weight_history))]),
        line_series_dict("Step 1", [step1_weight for _ in range(len(weight_history))]),
        line_series_dict("Step 2", [step2_weight for _ in range(len(weight_history))]),
        line_series_dict("Target weight", [target_weight for _ in range(len(weight_history))])
    ]
    weight_data['series'] = series
    weight_data['chartOptions'] = {
        "colors": ["#4285F4", "#DB4437", "#F4B400", "#b9ff00", "#0F9D58"],
        "chart": {
            "height": 500,
            "type": "line"
        },
        "stroke": {
            "width": [3, 3, 3, 3, 3],
            "dashArray": [0, 5, 5, 5, 5],
            "curve": "smooth"
        },
        "markers": {
          "size": [5, 0, 0, 0, 0]
        },
        "title": {
            "text": "Weight"
        },
        "dataLabels": {
            "enabled": True,
            "enabledOnSeries": []
        },
        "labels": [entry['display_date'] for entry in weight_history],
        "xaxis": {
            "type": "datetime"
        },
        "yaxis": [
            {
                "title": {
                    "text": "Weight (kg)"
                },
                "min": target_weight,
                "max": start_weight
            },
        ]
    }

    return weight_data


@app.post("/calories/entry/create")
def create_new_entry(
        entry: NewEntry
):
    metrics = {
        entry.field: entry.value
    }

    result = log_metrics_in_es(
        metrics=metrics,
        user_id="client",
        timestamp=entry.timestamp
    )
    return result


@app.post("/calories/entry/edit")
def delete_entry(
        body: EditEntry
):
    result = update_document_by_id(body.document_id, document_body=body.updatedDocument, index=body.index)
    return result


@app.post("/calories/entry/delete")
def delete_entry(
        body: DeleteEntry
):
    result = delete_document_by_id(body.document_id, index=body.index)
    return result


