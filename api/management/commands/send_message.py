from django.conf import settings

from api.models import Device
from django.core.management.base import BaseCommand

from pyfcm import FCMNotification


class Command(BaseCommand):
    help = 'send fcm message'

    def handle(self, *args, **kwargs):
        data_message = dict(type="url", message="hello",
                            title="hell", url="url",
                            click_action="FLUTTER_NOTIFICATION_CLICK")
        push_service = FCMNotification(api_key=settings.FCM_API_KEY)
        registration_ids = Device.objects.all().values_list("registration_id",
                                                            flat=True)
        registration_ids = list(set(list(registration_ids)))
        push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            message_title=data_message['type'],
            message_body=data_message["message"], data_message=data_message)
        self.stdout.write('Successfully send ..')
