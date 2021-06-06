import time

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse

from messaging_utils import get_pipeline_for_sms_command
from bio_metrics_utils import get_calorie_window_stats
from decorators import validate_user_auth_level, messaging_response

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


@app.post("/calories/entry/create")
def create_new_calorie_entry(
        calories: int
):
    print(calories)
    return {}




