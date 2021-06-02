"""
 Pipelines for processing data and performing an action
"""
from elasticsearch_utils import delete_document_by_id
from decorators import messaging_response, messaging_response_result
from bio_metrics_utils import log_metrics_in_es, get_calorie_window_stats
from pydantic_models import ResponseContent
from data_utils import parse_text_message


def create_summary_sms(
        data: dict
):
    history = data['history']
    summary_string = ''
    for entry in reversed(history):
        summary_string += f"{entry['display_date']} - {entry['calories']} calories\n"

    total_calories = data['summary']['total_calories']
    daily_average_calories = data['summary']['average_daily_calories']
    daily_average_difference = data['summary']['average_daily_difference']
    net_difference = data['summary']['net_difference']

    summary_string += "\n"
    summary_string += f"Total calories: {total_calories}\n"
    summary_string += f"Daily average: {daily_average_calories}\n"
    summary_string += f"Daily difference: {daily_average_difference}\n"
    summary_string += f"7 Day Difference: {net_difference}"

    return summary_string


@messaging_response
def sms_to_log_metric_pipeline(
        sms_body: str,
        from_: str,
        timestamp: int
) -> str:
    """
    Takes information in a sms message and stores the appropriate metric in the database
    :param sms_body:
    :param from_:
    :param timestamp:
    :return:
    """
    metrics = parse_text_message(sms_body)
    result = log_metrics_in_es(metrics, user_id=from_, timestamp=timestamp)
    return "Metrics logged successfully!"


@messaging_response_result
def sms_to_calorie_summary_pipeline(
        *args,
        **kwargs
) -> str:
    """
    Takes information in a sms message and returns the calorie intake summary for the past 7 days
    :param args:
    :param kwargs:
    :return:
    """
    response_content: ResponseContent = get_calorie_window_stats()
    data = response_content.data

    return create_summary_sms(data)


@messaging_response_result
def sms_to_what_if_calorie_pipeline(
        sms_body: str,
        from_: str,
        timestamp: int
):
    # replace the 'if' part so that we can use this function like we would in a regular situation
    sms_body = sms_body.replace("if", '')
    metrics = parse_text_message(sms_body)

    # log this as a "tomorrow" event to not mess with the counting
    # TODO better way to do this overall
    timestamp += 24 * 3600
    result = log_metrics_in_es(metrics, user_id=from_, timestamp=timestamp, document_id="document-to-delete")
    response_content: ResponseContent = get_calorie_window_stats()
    data = response_content.data

    summary_text = create_summary_sms(data)
    result = delete_document_by_id("document-to-delete", index="road83-metric-logs")
    return summary_text

