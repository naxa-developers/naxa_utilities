from django.conf import settings
from pyfcm import FCMNotification


def send_message(data_message, registration_ids):
    push_service = FCMNotification(api_key=settings.FCM_API_KEY)
    push_service.multiple_devices_data_message(
        registration_ids=registration_ids, data_message=data_message)
