"""
Functions that make working with dates easier
"""
from typing import *
import datetime
from datetime import datetime as dt
import dateutil


def get_date(
        delta: float = 0.0,
        delta_format: Optional[str] = "days",
        str_format: Optional[str] = None,
        return_timestamp: bool = False,
        timestamp_formatter: callable = int
) -> Union[datetime.datetime, float]:
    """
    A convenience function that returns a date or a unix timestamp and allows for specifying time deltas
    :param delta:
    :param delta_format:
    :param str_format:
    :param return_timestamp:
    :param timestamp_formatter:
    :return:
    """
    today = dt.now()
    time_delta = datetime.timedelta(days=0)
    if delta:
        kwargs = {delta_format: delta}
        time_delta = datetime.timedelta(**kwargs)
    output_date = today - time_delta

    if str_format:
        output_date = output_date.strftime(str_format)

    if return_timestamp:
        output_date = timestamp_formatter(output_date.timestamp())

    return output_date


def get_yesterday(**kwargs) -> Union[datetime.datetime, float]:
    """
    Returns the date for yesterday
    :param kwargs:
    :return:
    """
    # make sure certain parameters are not over-written or specified twice
    kwargs.pop('delta', None)
    kwargs.pop('delta_format', None)
    return get_date(delta=1, **kwargs)
