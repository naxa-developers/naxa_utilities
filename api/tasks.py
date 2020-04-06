from __future__ import absolute_import, unicode_literals

import os

import pandas as pd
import time

from celery import shared_task
from uuid import uuid4

from api.management.commands.generate_excel import travel_data
from api.models import CeleryTaskProgress, UserReport
from api.utils import *


@shared_task()
def add(x, y):
    print("hello")
    return x + y


@shared_task()
def generate_user_report(pk):
    time.sleep(5)
    task = CeleryTaskProgress.objects.get(pk=pk)
    task.status = 1
    task.save()
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
    df.to_excel(settings.MEDIA_ROOT + "/user_assessment_latest.xlsx")
    task.file.name = settings.MEDIA_ROOT + "/user_assessment_latest.xlsx"
    task.status = 2
    task.save()


