from django.core.management.base import BaseCommand
import pandas as pd
from api.models import MedicalFacility, MedicalFacilityType, \
    MedicalFacilityCategory, Province, Municipality, District


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']

