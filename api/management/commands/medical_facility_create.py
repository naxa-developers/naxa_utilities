from django.contrib.gis.geos import Point
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
        Municipality.objects.all().delete()
        District.objects.all().delete()
        MedicalFacility.objects.all().delete()

        dfd = pd.read_excel("data_csv/data.xlsx", sheet_name="District Data")
        for index, row in dfd.iterrows():
            District.objects.get_or_create(
                province=Province.objects.get(province_id=row['Province_id']),
                district_id=row['District_id'], name=row['District_name'])

            dfm = pd.read_excel(path, sheet_name="Municipality Data")
        for index, row in dfm.iterrows():
            Municipality.objects.get_or_create(mun_id=row['HLCIT_Code'],
                province=Province.objects.get(province_id=row['Province_id']),
                district=District.objects.get(district_id=row['District_id']),
                name=row['Palika_Name'])

        df = pd.read_excel(path, sheet_name="Facility Data")
        new_objects = []
        old_objects = []
        for index, row in df.iterrows():
            if row["id"]:
                print(row)
                m = Municipality.objects.get(mun_id=row["mun_id"])
                new_ob = MedicalFacility(municipality=m, name=row["name"],
                    category=MedicalFacilityCategory.objects.get(pk=row[
                        "category"]), type=MedicalFacilityType.objects.get(
                        pk=row["type"]), ownership=row["ownership"],
                    contact_person=row["contact_person"],
                         contact_num=row["contact_num"],
                     used_for_corona_response=row['used_for_corona_response'],
                                         num_of_bed=row[
                        "num_of_bed"], num_of_icu_bed=row["num_of_icu_bed"],
                    occupied_icu_bed=row["occupied_icu_bed"],
                    num_of_ventilators=row["num_of_ventilators"],
                    occupied_ventilators=row["occupied_ventilators"],
                    num_of_isolation_bed=row["num_of_isolation_bed"],
                    occupied_isolation_bed=row["occupied_isolation_bed"],
                    total_tested=row["total_tested"], total_positive=row[
                        "total_positive"], total_death=row["total_death"],
                    total_in_isolation=row["total_in_isolation"], hlcit_code=row[
                        "hlcit_code"], remarks=row["remarks"], lat=row["lat"],
                    long=row["long"])
                new_ob.location = Point(x=new_ob.long, y=new_ob.lat, srid=4326)
                new_ob.district = m.district
                new_ob.province = m.province
                new_objects.append(new_ob)
            else:
                old_obj = MedicalFacility.objects.get(pk=row["id"])
                old_obj.ownership = row["ownership"]
                old_obj.contact_person = row["contact_person"]
                old_obj.contact_num = row["contact_num"]
                old_obj.used_for_corona_response = row[
                    "used_for_corona_response"]
                old_obj.num_of_bed = row["num_of_bed"]
                old_obj.num_of_icu_bed = row["num_of_icu_bed"]
                old_obj.occupied_icu_bed = row["occupied_icu_bed"]
                old_obj.num_of_ventilators = row["num_of_ventilators"]
                old_obj.occupied_ventilators = row["occupied_ventilators"]
                old_obj.num_of_isolation_bed = row["num_of_isolation_bed"]
                old_obj.occupied_isolation_bed = row["occupied_isolation_bed"]
                old_obj.total_tested = row["total_tested"]
                old_obj.total_positive = row["total_positive"]
                old_obj.total_death = row["total_death"]
                old_obj.total_in_isolation = row[
                "total_in_isolation"]
                old_obj.hlcit_code = row["hlcit_code"]
                old_obj.remarks = row["remarks"]
                old_obj.lat = row["lat"]
                old_obj.long = row["long"]
                old_obj.location = Point(x=old_obj.long, y=old_obj.lat, srid=4326)
                old_objects.append(old_obj)

        MedicalFacility.objects.bulk_create(new_objects)
        MedicalFacility.objects.bulk_update(old_objects, ['ownership',
                      'contact_person', 'contact_num',
                      'used_for_corona_response', 'num_of_bed',
                                                          'occupied_ventilators', 'num_of_ventilators', 'occupied_icu_bed', 'num_of_icu_bed', 'hlcit_code', 'total_positive', 'total_death', 'total_in_isolation', 'occupied_isolation_bed', 'total_tested', 'num_of_isolation_bed', 'remarks', 'lat', 'long'])
