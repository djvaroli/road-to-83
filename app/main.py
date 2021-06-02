import time

from fastapi import FastAPI, Form, HTTPException

from messaging_utils import get_pipeline_for_sms_command
from bio_metrics_utils import get_calorie_window_stats
from decorators import validate_user_auth_level, messaging_response
from pydantic_models import ResponseContent

app = FastAPI()


@app.get("/")
@app.get("/home")
def home():
    """
    The home page of the app. May the force be with you!
    :return:
    """
    return "Hello there!"


@app.post("/interact/sms", status_code=201)
@messaging_response("Success!")
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
    response_content: ResponseContent = pipeline(Body, From, timestamp)
    if response_content.status != "success":
        raise HTTPException(status_code=500, detail=response_content.error_message)

    return response_content


@app.post("/notify/error", status_code=200)
@messaging_response("An error occurred.")
def notify_user_of_error(*args, **kwargs):
    return


@app.get("/history/window_calories")
def get_calorie_stats_in_window(
        windowSizeDays: int = 7
):
    stats = get_calorie_window_stats(window_size_days=windowSizeDays)
    print(stats)
    return stats




