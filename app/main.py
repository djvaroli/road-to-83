import time
from typing import *

from fastapi import FastAPI, Form, Response, HTTPException
from twilio.twiml.messaging_response import MessagingResponse

from app.utilities.bio_metrics_utils import log_metrics_in_redis, log_metrics_in_es
from app.utilities.data_utils import parse_text_message
from app.utilities.decorators import validate_user_auth_level, notify_user_if_failed

app = FastAPI()


@app.get("/", status_code=200)
@app.get("/home", status_code=200)
def home():
    return "Hello there!"


@app.post("/record", status_code=201)
# @notify_user_if_failed
@validate_user_auth_level(level=5, field="From")
def record_weight(
        From: str =  Form(default=None),
        Body: str = Form(default=None),
        timestamp: int = int(time.time()),
        index: Optional[str] = None
):
    metrics = parse_text_message(Body)
    result, status, message = log_metrics_in_es(metrics, user_id=From, timestamp=timestamp, index=index)
    message_response = MessagingResponse()

    if status != "ok":
        raise HTTPException(status_code=500, detail=message)

    msg = message_response.message("Metrics logged successfully!")
    return message_response





