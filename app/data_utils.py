import re


VALID_LOGGING_FIELDS = [
    'weight', "calories"
]

FIELD_PROCESSING_OP = {
    "weight": float,
    "calories": float
}


def parse_text_message(
        body: str
):
    """
    So far assume that only weight is logged
    :param body:
    :return:
    """
    message_clean = clean_and_split_string(body.lower().strip())
    assert len(message_clean) <= 2
    assert message_clean[0] in VALID_LOGGING_FIELDS

    processing_operation = FIELD_PROCESSING_OP.get(message_clean[0])
    result = {
        message_clean[0]: processing_operation(message_clean[1])
    }

    return result


def clean_and_split_string(
        s: str,
        split_char: str = " "
):
    return re.sub('[^A-Za-z0-9\.]+', ' ', s).lower().split(split_char)
