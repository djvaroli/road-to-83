"""
 pipelines for processing data and performing an action
"""

from bio_metrics_utils import log_metrics_in_es, get_calorie_window_stats
from pydantic_models import ResponseContent
from data_utils import parse_text_message


def sms_to_log_metric_pipeline(
        sms_body: str,
        from_: str,
        timestamp: int
) -> ResponseContent:
    """
    Takes information in a sms message and stores the appropriate metric in the database
    :param sms_body:
    :param from_:
    :param timestamp:
    :return:
    """
    metrics = parse_text_message(sms_body)
    return log_metrics_in_es(metrics, user_id=from_, timestamp=timestamp)


def sms_to_calorie_summary_pipeline(
        *args,
        **kwargs
) -> ResponseContent:
    """
    Takes information in a sms message and returns the calorie intake summary for the past 7 days
    :param args:
    :param kwargs:
    :return:
    """
    response_content: ResponseContent = get_calorie_window_stats()
    data = response_content.data
    history = data['history']
    print(history)
    return response_content
