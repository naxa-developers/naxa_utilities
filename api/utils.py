from django.conf import settings
from pyfcm import FCMNotification


def send_message(data_message, registration_ids):
    pass
    # push_service = FCMNotification(api_key=settings.FCM_API_KEY)
    # push_service.notify_multiple_devices(
    #     registration_ids=registration_ids, message_title=data_message['type'],
    #     message_body=data_message["message"], data_message=data_message)
