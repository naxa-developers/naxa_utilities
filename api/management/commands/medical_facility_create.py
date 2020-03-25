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
        MedicalFacility.objects.all().delete()
        ownership_dict = dict(MedicalFacility.OWNERSHIP_CHOICES)
        ownership_replace = {y: x for x, y in ownership_dict.items()}
        ownership_replace['NAN'] = "0"
        ownership_replace['nan'] = "0"
        df = pd.read_csv(path)
        upper_range = len(df)
        df.fillna({'ownership': "0", 'Longitude': 85.3240, 'Latitude': 85.3240,
                   'No_of_Beds': 0, 'Number_of_ICU_Wards':0,
                   'Number_of_Ventilators': 0, 'Number_of_Isolation_Beds':0,
                   'Remaining_Capacity': 0, 'Used_for_Corona_Response':False,
                   'Type':"Hospital"},
                  inplace=True)
        df.replace({"ownership": ownership_replace}, inplace=True)
        df.replace({"Used_for_Corona_Response": {"Yes": True,
                                                 'No': False}}, inplace=True)
        print("Wait Data is being Loaded")
        medical_fac = [
            MedicalFacility(
                type=MedicalFacilityType.objects.get(name=str((df[
                    'Type'][
                    row]))),
                category=MedicalFacilityCategory.objects.get(name=str((df[
                    'Category'][
                    row]))),
                province=Province.objects.get(name=str((df[
                    'Province'][
                    row]))),
                municipality=Municipality.objects.get(name=str((df[
                    'Municipality'][
                    row]))),
                district=District.objects.get(name=str((df[
                    'District'][
                    row]))),
                name=str(df['Name of Facility'][row]),
                ownership=str(df['Type_of_Ownership'][row]),
                contact_num=str(df['Contact_No'][row]),
                used_for_corona_response=df['Used_for_Corona_Response'][row],
                num_of_bed=int(df['No_of_Beds'][row]),
                num_of_ventilators=int(df['Number_of_Ventilators'][row]),
                num_of_isolation_bed=int(df['Number_of_Isolation_Beds'][row]),
                remarks=str(df['Remarks'][row]),
                lat=float(df['Latitude'][row]),
                long=float(df['Longitude'][row]),

            ) for row in range(0, upper_range)
        ]
        medical = MedicalFacility.objects.bulk_create(medical_fac)

        if medical:
            self.stdout.write('Successfully loaded Medical Value  ..')
