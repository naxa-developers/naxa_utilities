import datetime
from django.contrib.gis.db import models


class MedicalFacilityCategory(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class MedicalFacilityType(models.Model):
    category = models.ForeignKey(MedicalFacilityCategory, on_delete=models.CASCADE, related_name='Category')
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    province_id = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class MedicalFacility(models.Model):
    OWNERSHIP_CHOICES = (
        ('0', 'UNKNOWN'),
        ('1', 'GOVERNMENT'),
        ('2', 'PRIVATE'),

    )
    province = models.ForeignKey(Province, on_delete=models.CASCADE,
                                    related_name='medical_facility',
                                 blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                    related_name='medical_facility', blank=True, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE,
                                    related_name='medical_facility', blank=True, null=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(MedicalFacilityCategory,
                                 on_delete=models.CASCADE,
                                 related_name='medical_facility', blank=True, null=True)
    type = models.ForeignKey(MedicalFacilityType, on_delete=models.CASCADE, related_name='Type')
    ownership = models.CharField(max_length=300, default="0", choices=OWNERSHIP_CHOICES)
    contact_person = models.CharField(max_length=500, null=True, blank=True)
    contact_num = models.CharField(max_length=500, null=True, blank=True)
    used_for_corona_response = models.BooleanField(default=True)
    num_of_bed = models.IntegerField(null=True, blank=True, default=0)
    num_of_icu_bed = models.IntegerField(null=True, blank=True, default=0)
    occupied_icu_bed = models.IntegerField(null=True, blank=True, default=0)
    num_of_ventilators = models.IntegerField(null=True, blank=True, default=0)
    occupied_ventilators = models.IntegerField(null=True, blank=True, default=0)
    num_of_isolation_bed = models.IntegerField(null=True, blank=True, default=0)
    occupied_isolation_bed = models.IntegerField(null=True, blank=True,
                                                default=0)
    total_tested = models.IntegerField(null=True, blank=True, default=0)
    total_positive = models.IntegerField(null=True, blank=True, default=0)
    total_death = models.IntegerField(null=True, blank=True, default=0)
    total_in_isolation = models.IntegerField(null=True, blank=True, default=0)
    hlcit_code = models.CharField(max_length=63, null=True, blank=True)
    remarks = models.TextField(blank=True)
    location = models.PointField(srid=4326, blank=True, null=True)
    lat = models.FloatField(null=True, blank=True, default=0)
    long = models.FloatField(null=True, blank=True, default=0)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.lat = self.location.y
        self.long = self.location.x
        super(MedicalFacility, self).save(*args, **kwargs)


class ProvinceData(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='Province')
    num_of_bed = models.IntegerField(null=True, blank=True, default=0)
    num_of_icu_bed = models.IntegerField(null=True, blank=True, default=0)
    occupied_icu_bed = models.IntegerField(null=True, blank=True, default=0)
    num_of_ventilators = models.IntegerField(null=True, blank=True, default=0)
    occupied_ventilators = models.IntegerField(null=True, blank=True, default=0)
    num_of_isolation_bed = models.IntegerField(null=True, blank=True, default=0)
    occupied_isolation_bed = models.IntegerField(null=True, blank=True,
                                                 default=0)
    total_tested = models.IntegerField(null=True, blank=True, default=0)
    total_positive = models.IntegerField(null=True, blank=True, default=0)
    total_death = models.IntegerField(null=True, blank=True, default=0)
    total_in_isolation = models.IntegerField(null=True, blank=True, default=0)
    active = models.BooleanField(default=True)
    update_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            now = datetime.datetime.now()
            province = self.province_id
            ProvinceData.objects.filter(active=True, province_id=province).update(
                active=False, update_date=now)
        super().save(*args, **kwargs)

class CovidCases(models.Model):
    total_tested = models.IntegerField(null=True, blank=True, default=0)
    tested_positive = models.IntegerField(null=True, blank=True, default=0)
    tested_negative = models.IntegerField(null=True, blank=True, default=0)
    death = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateField(null=True, blank=True)


