from django.core.management.base import BaseCommand
from api.models import ProvinceData, MuniData, DistrictData, Province, \
    District, Municipality


class Command(BaseCommand):
    help = 'create default groups'

    def handle(self, *args, **kwargs):
        province_list = Province.objects.all()
        district_list = District.objects.all()
        municipality_list = Municipality.objects.all()

        for p in province_list:
            ProvinceData.objects.get_or_create(active=True, province_id=p)
        for d in district_list:
            DistrictData.objects.get_or_create(district_id=d, active=True)
        for m in municipality_list:
            MuniData.objects.get_or_create(municipality_id=m, active=True)
        print("created")

