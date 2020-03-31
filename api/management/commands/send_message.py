from api.models import Device
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'send fcm message'

    def handle(self, *args, **kwargs):
        self.stdout.write('Successfully created ..')
