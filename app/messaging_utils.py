"""
Utility functions for messaging interactions
"""

from twilio.twiml.messaging_response import MessagingResponse

from data_utils import clean_and_split_string
from pipelines import sms_to_log_metric_pipeline, track_metric_pipeline, sms_to_what_if_calorie_pipeline

SMS_COMMAND_OPERATION = {
    "track": track_metric_pipeline,
    "if": sms_to_what_if_calorie_pipeline
}


def get_messaging_response(
        message: str = None
):
    """
    Helper function returning an instance of the twilio.twiml.messaging_response.MessagingResponse object
    :param message:
    :return:
    """
    messaging_response = MessagingResponse()
    if message:
        messaging_response.message(message)

    return messaging_response


def get_pipeline_for_sms_command(
        sms_body: str
):
    """
    Returns the correct pipeline for processing an sms request
    :param sms_body:
    :return:
    """
    command, *command_args = clean_and_split_string(sms_body)

    pipeline = SMS_COMMAND_OPERATION.get(command)
    if pipeline is None:
        raise ValueError(f"Invalid command {command}.")

    return pipeline
