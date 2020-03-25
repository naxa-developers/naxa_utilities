from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

GROUPS = ["User", "Facility", "Province"]

class Command(BaseCommand):
    help = 'create default groups'

    def handle(self, *args, **kwargs):
        for g in GROUPS:
            Group.objects.get_or_create(name=g)
        self.stdout.write('Successfully created ..')
