from django.core.management.base import BaseCommand
import pandas as pd
from api.models import MedicalFacility, MedicalFacilityType, \
    MedicalFacilityCategory, Province, Municipality, District, AgeGroupData


class Command(BaseCommand):
    help = 'load age data from file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        AgeGroupData.objects.all().delete()
        df = pd.read_csv(path)
        df['0_14'] = df['0_14'].str.replace(',', '').astype(int)
        df['15_49'] = df['15_49'].str.replace(',', '').astype(int)
        df['50+'] = df['50+'].str.replace(',', '').astype(int)
        df['Total'] = df['Total'].str.replace(',', '').astype(int)
        df['munid'] = pd.to_numeric(df['munid'], errors='coerce')
        df['provinceId'] = pd.to_numeric(df['provinceId'], errors='coerce')
        df['districtId'] = pd.to_numeric(df['districtId'], errors='coerce')
        df = df.fillna(0)
        upper_range = len(df)
        print(upper_range, "UPPERRRRRRRRRRRRRRRRR   ")

        municipalities = list(df.Municipality.unique())
        for m in municipalities:
            Municipality.objects.get_or_create(name=m)

        districts = list(df.District.unique())
        for m in districts:
            District.objects.get_or_create(name=m)
        print("Wait Data is being Loaded")
        objects = [
            AgeGroupData(
                municipality=Municipality.objects.get(name=str((df[
                    'Municipality'][
                    row]))),
                district=District.objects.get(name=str((df[
                    'District'][
                    row]))),
                hlcit_code=str(df['HLCIT CODE'][row]),
                pcode=str(df['Pcode'][row]),
                l0_14=int(df['0_14'][row]),
                munid=int(df['munid'][row]),
                districtId=int(df['districtId'][row]),
                provinceId=int(df['provinceId'][row]),
                l15_49=int(df['15_49'][row]),
                l50plus=int(df['50+'][row]),
                ltotal=int(df['Total'][row]),

            ) for row in range(0, upper_range)
        ]
        medical = AgeGroupData.objects.bulk_create(objects)

        if medical:
            self.stdout.write('Successfully loaded Medical Value  ..')
