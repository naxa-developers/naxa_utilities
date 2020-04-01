import pandas as pd
from api.models import UserReport, MedicalFacility
from django.core.management.base import BaseCommand


def get_result(r):
    if r.has_convid_contact or r.has_travel_history:
        return "morelikely"
    elif r.temperature >= 102 and r.have_cough:
        return "likely"
    elif r.temperature >= 102 and r.have_fatigue:
        return "likely"
    elif r.temperature >= 102 and r.fast_breathe:
        return "likely"
    else:
        return "lesslikely"


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
                       'symptoms', 'has_convid_contact', 'has_travel_history']

            query = UserReport.objects.all().values(*columns)
            df = pd.DataFrame(query, columns=columns)
            df['result'] = df.apply(get_result, axis=1)
            df.to_excel("output.xlsx")
        elif report_type == "facility":
            columns = ['province', 'district', 'municipality', 'name',
                       'category', 'type', 'ownership', 'contact_person',
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



        
