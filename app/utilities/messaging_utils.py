from twilio.twiml.messaging_response import MessagingResponse


def get_messaging_response(
        message: str = None
):
    messaging_response = MessagingResponse()
    if message:
        messaging_response.message(message)

    return messaging_response