import json
import pandas as pd
from api.models import UserReport, MedicalFacility
from django.core.management.base import BaseCommand


def travel_data(r):
    travel_history = r.travel_history
    try:
        data = json.loads(travel_history)
        if not isinstance(data, dict):
            data = {}
    except:
        data = {}
    country_name = data.get('country_name', '')
    flight_name = data.get('flight_name', '')
    transit_names = data.get('transit_names', '')
    return country_name, flight_name, transit_names


class Command(BaseCommand):
    help = 'create excel report'

    def add_arguments(self, parser):
        parser.add_argument('report_type', type=str)

    def handle(self, *args, **kwargs):
        report_type = kwargs.get('report_type', "userreport")
        if report_type == "userreport":
            columns = ['lat', 'long', 'name', 'age', 'gender', 'temperature',
                       'in_self_quarrantine', 'have_cough', 'have_fatigue',
                       'have_throat_pain', 'fast_breathe', 'body_pain',
                       'diarrahoe', 'vomit', 'runny_nose', 'address',
                       'contact_no',
                       'symptoms', 'has_convid_contact',
                       'has_travel_history', 'result', 'travel_history']

            query = UserReport.objects.all().values(*columns)
            df = pd.DataFrame(query, columns=columns)
            df[['country_name', 'flight_name', 'transit_names']] = df.apply(
                travel_data, axis=1, result_type="expand")
            del df['travel_history']
            df.to_excel("output.xlsx")
        elif report_type == "facility":
            columns = ['id', 'province', 'province__name', 'district',
                      'district__name', 'municipality', 'municipality__name',
                      'name', 'category',
                       'category__name', 'type', 'type__name', 'ownership',
                       'contact_person',
                       'contact_num', 'used_for_corona_response',
                       'num_of_bed', 'num_of_icu_bed', 'occupied_icu_bed',
                       'num_of_ventilators', 'occupied_ventilators',
                       'num_of_isolation_bed', 'occupied_isolation_bed',
                       'total_tested', 'total_positive', 'total_death',
                       'total_in_isolation', 'hlcit_code', 'remarks', 'lat',
                       'long']
            query = MedicalFacility.objects.all().values(*columns)
            df = pd.DataFrame(query, columns=columns)
            df.to_excel("medical_facility.xlsx")

