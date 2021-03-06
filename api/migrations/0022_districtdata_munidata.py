# Generated by Django 2.2.10 on 2020-03-26 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20200326_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='MuniData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_of_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('num_of_icu_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('occupied_icu_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('num_of_ventilators', models.IntegerField(blank=True, default=0, null=True)),
                ('occupied_ventilators', models.IntegerField(blank=True, default=0, null=True)),
                ('num_of_isolation_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('occupied_isolation_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('total_tested', models.IntegerField(blank=True, default=0, null=True)),
                ('total_positive', models.IntegerField(blank=True, default=0, null=True)),
                ('total_death', models.IntegerField(blank=True, default=0, null=True)),
                ('total_in_isolation', models.IntegerField(blank=True, default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('update_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('hotline', models.TextField()),
                ('district_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='muncdata', to='api.District')),
                ('municipality_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='muncdata', to='api.Municipality')),
                ('province_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='muncdata', to='api.Province')),
            ],
        ),
        migrations.CreateModel(
            name='DistrictData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_of_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('num_of_icu_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('occupied_icu_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('num_of_ventilators', models.IntegerField(blank=True, default=0, null=True)),
                ('occupied_ventilators', models.IntegerField(blank=True, default=0, null=True)),
                ('num_of_isolation_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('occupied_isolation_bed', models.IntegerField(blank=True, default=0, null=True)),
                ('total_tested', models.IntegerField(blank=True, default=0, null=True)),
                ('total_positive', models.IntegerField(blank=True, default=0, null=True)),
                ('total_death', models.IntegerField(blank=True, default=0, null=True)),
                ('total_in_isolation', models.IntegerField(blank=True, default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('update_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('hotline', models.TextField()),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district_data', to='api.District')),
                ('province_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district_data', to='api.Province')),
            ],
        ),
    ]
