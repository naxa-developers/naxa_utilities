# Generated by Django 2.2.10 on 2020-04-02 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_remove_municipality_municipality_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipality',
            name='municipality_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
