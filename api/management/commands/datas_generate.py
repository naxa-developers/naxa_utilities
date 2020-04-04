from django.core.management.base import BaseCommand
from api.models import ProvinceData, MuniData, DistrictData, Province, \
    District, Municipality, UserReport


class Command(BaseCommand):
    help = 'create default datas /setup'

    def handle(self, *args, **kwargs):
        # province_list = Province.objects.all()
        # district_list = District.objects.all()
        # municipality_list = Municipality.objects.all()
        report_list = UserReport.objects.all()

        # for p in province_list:
        #     ProvinceData.objects.get_or_create(active=True, province_id=p)
        # for d in district_list:
        #     DistrictData.objects.get_or_create(district_id=d, active=True)
        # for m in municipality_list:
        #     MuniData.objects.get_or_create(municipality_id=m, active=True)
        # print("created")

        for r in report_list:
            r.save()


