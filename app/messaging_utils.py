from twilio.twiml.messaging_response import MessagingResponse

from data_utils import clean_and_split_string
from bio_metrics_utils import get_calorie_window_stats, log_metrics_in_es
from pipelines import sms_to_log_metric_pipeline


SMS_COMMAND_OPERATION = {
    "summary": get_calorie_window_stats,
    "calories": sms_to_log_metric_pipeline,
    "weight": sms_to_log_metric_pipeline
}


def get_messaging_response(
        message: str = None
):
    messaging_response = MessagingResponse()
    if message:
        messaging_response.message(message)

    return messaging_response


def get_pipeline_for_sms_command(
        sms_body: str
):
    sms_body_split = clean_and_split_string(sms_body)
    command = sms_body_split[0]

    pipeline = SMS_COMMAND_OPERATION.get(command)
    if pipeline is None:
        raise ValueError(f"Invalid command {command}.")

    return pipeline
