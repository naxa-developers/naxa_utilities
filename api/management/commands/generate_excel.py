import pandas as pd
from api.models import UserReport
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


columns = ['lat', 'long', 'name', 'age', 'gender', 'temperature',
           'in_self_quarrantine', 'have_cough', 'have_fatigue',
           'have_throat_pain', 'fast_breathe','body_pain',
           'diarrahoe', 'vomit', 'runny_nose', 'address', 'contact_no',
           'symptoms', 'has_convid_contact', 'has_travel_history']


class Command(BaseCommand):
    help = 'create excel report'

    def handle(self, *args, **kwargs):
        query = UserReport.objects.all().values(*columns)
        df = pd.DataFrame(query, columns=columns)
        df['result'] = df.apply(get_result, axis=1)
        df.to_excel("output.xlsx")


        
