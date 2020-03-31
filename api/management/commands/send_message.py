from django.conf import settings

from api.models import Device
from django.core.management.base import BaseCommand

from pyfcm import FCMNotification


class Command(BaseCommand):
    help = 'send fcm message'

    def handle(self, *args, **kwargs):
        data_message = {
            "Nick": "Mario",
            "body": "great match!",
            "Room": "PortugalVSDenmark"
        }
        push_service = FCMNotification(api_key=settings.FCM_API_KEY)
        registration_ids = Device.objects.all().values_list("device_id",
                                                            flat=True)
        result = push_service.multiple_devices_data_message(
            registration_ids=registration_ids, data_message=data_message)
        self.stdout.write('Successfully created ..')
        print(result)
