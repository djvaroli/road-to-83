import time
from typing import *

from fastapi import FastAPI, Form, HTTPException

from app.utilities.bio_metrics_utils import log_metrics_in_es
from app.utilities.data_utils import parse_text_message
from app.utilities.decorators import validate_user_auth_level, messaging_response
from app.utilities.messaging_utils import get_messaging_response
from app.utilities.pydantic_models import ResponseContent

app = FastAPI()


@app.get("/", status_code=200)
@app.get("/home", status_code=200)
def home():
    return "Hello there!"


@app.post("/record", status_code=201)
@messaging_response("Metrics stored successfully!")
@validate_user_auth_level(level=5, field="From")
def record_weight(
        From: str =  Form(default=None),
        Body: str = Form(default=None),
        timestamp: int = int(time.time())
):
    metrics = parse_text_message(Body)
    response_content: ResponseContent = log_metrics_in_es(metrics, user_id=From, timestamp=timestamp)
    if response_content.status != "success":
        raise HTTPException(status_code=500, detail=response_content.error_message)

    return response_content


@app.post("/notify/error", status_code=200)
@messaging_response("An error occurred.")
def notify_user_of_error(*args, **kwargs):
    return





