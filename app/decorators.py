from functools import wraps

from fastapi import HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse

from auth_utils import get_user_auth_level
from logging_utils import get_logger
from pydantic_models import ResponseContent


logger = get_logger(__name__)


def add_request_status_info(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            data = f(*args, **kwargs)
            status = "success"
            error = None
        except Exception as e:
            data = None
            status = "failed"
            error = e

        return ResponseContent(data=data, error_message=error, status=status)
    return wrapped


def validate_user_auth_level(level: int, field: str):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_identifier = kwargs.get(field)
            user_auth_level = get_user_auth_level(user_identifier)
            if user_auth_level < level:
                raise HTTPException(status_code=401, detail="You are unauthorized to access this resource!")

            return f(*args, **kwargs)

        return wrapped
    return wrapper


def messaging_response(
        message: str,
        media_type: str = "text/xml"
):
    """
    Takes the result string and converts into a twilio Messaging Response to be returned by the API
    :param message:
    :param media_type:
    :return:
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            message_response = MessagingResponse()
            result = f(*args, **kwargs)
            msg = message_response.message(message)

            return Response(content=str(message_response), media_type=media_type)
        return wrapped
    return wrapper


def messaging_response_result(f):
    """
    Takes the result string and converts into a twilio Messaging Response to be returned by the API
    :param: f
    :return:
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        message_response = MessagingResponse()
        message = f(*args, **kwargs)
        msg = message_response.message(message)

        return Response(content=str(message_response), media_type="text/xml")
    return wrapped


