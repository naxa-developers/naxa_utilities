from django.core.management.base import BaseCommand
import pandas as pd
from api.models import MedicalFacility, MedicalFacilityType, MedicalFacilityCategory


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        df = pd.read_csv(path)
        upper_range = len(df)
        print("Wait Data is being Loaded")

        # try:
        #     for row in range(0, upper_range):
        #         print((df['Number_of_ICU_Wards'][row]))
        #         print(int(df['Remaining_Capacity'][row]))
        #         print(df['SN'][row])
        #
        #         # type = MedicalFacilityType.objects.get(name=str((df['Type'][row]))),
        #
        #     if palika_update:
        #         self.stdout.write('Successfully  updated data ..')
        #
        #
        # except Exception as e:
        #     print(e)

        try:
            medical_fac = [
                MedicalFacility(
                    type=MedicalFacilityType.objects.get(name=str((df['Type'][row]))),
                    name=str(df['Name of Facility'][row]),
                    ownership=str(df['Type_of_Ownership'][row]),
                    contact_num=str(df['Contact_No'][row]),
                    is_used_for_Corona_response=str(df['Used_for_Corona_Response'][row]),
                    num_of_bed=int(df['No_of_Beds'][row]),
                    num_of_icu_ward=int(df['Number_of_ICU_Wards'][row]),
                    num_of_ventilators=int(df['Number_of_Ventilators'][row]),
                    num_of_isolation_ward=int(df['Number_of_Isolation_Wards'][row]),
                    remaining_capacity=int(df['Remaining_Capacity'][row]),
                    remarks=str(df['Remarks'][row]),
                    lat=float(df['Latitude'][row]),
                    long=float(df['Longitude'][row]),

                ) for row in range(0, upper_range)
            ]
            medical = MedicalFacility.objects.bulk_create(medical_fac)

            if medical:
                self.stdout.write('Successfully loaded Medical Value  ..')
                # print((df['paulika_name'][row]).capitalize())
                # a = GapaNapa.objects.get(name=str((df['paulika_name'][row]).capitalize().strip()))
                # print(a)
                # print((df['indicators'][row]).strip())
                # a = Indicator.objects.get(indicator=str((df['indicators'][row]).strip()))
                # print(a)


        except Exception as e:
            print(e)
