# Generated by Django 2.2.10 on 2020-03-22 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_covidcases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covidcases',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
