from functools import wraps

from fastapi import HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse

from app.utilities.auth_utils import get_user_auth_level
from app.utilities.logging_utils import get_logger


logger = get_logger(__name__)


def request_status(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            status = "ok"
            message = "Operation completed successfully!"
        except TimeoutError as e:
            result = None
            status = "failed"
            message = "Operation timed out, try again later!"
        except Exception as e:
            result = None
            status = "failed"
            message = "A server-side error occurred!"

        return result, status, message
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


def notify_user_if_failed(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        rsp = MessagingResponse()
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            logger.warning(e)
            msg = rsp.message("A server-side error occurred.")
            return rsp

        return result
    return wrapped


