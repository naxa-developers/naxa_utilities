import datetime
import json
from django.contrib.auth.models import Group
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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
    province = models.ForeignKey(Province, on_delete=models.CASCADE,
                                 related_name='districts',
                                 blank=True, null=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE,
                                 related_name='municipalities',
                                 blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 related_name='municipalities',
                                 blank=True, null=True)

    def __str__(self):
        return self.name


class MedicalFacility(models.Model):
    OWNERSHIP_CHOICES = (
        ('0', 'Unknown'),
        ('1', 'Government'),
        ('2', 'Private'),
        ('3', 'Nepal Army'),
        ('nan', 'Unknown'),

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
        if self.location:
            self.lat = self.location.y
            self.long = self.location.x
        elif self.lat and self.long:
            self.location = Point(x=self.long, y=self.lat, srid=4326)
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
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    hotline = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:
            now = datetime.datetime.now()
            province = self.province_id
            ProvinceData.objects.filter(active=True, province_id=province).update(
                active=False, update_date=now)
        super().save(*args, **kwargs)


class DistrictData(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE,
                                    related_name='district_data', null=True, blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE,
                          related_name='district_data')
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
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    hotline = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:
            now = datetime.datetime.now()
            district = self.district_id
            DistrictData.objects.filter(active=True, district_id=district).update(
                active=False, update_date=now)
            if self.district_id.province:
                self.province_id = self.district_id.province
        super().save(*args, **kwargs)


class MuniData(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE,
                                    related_name='muncdata', blank=True,
                                    null=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE,
                          related_name='muncdata', null=True, blank=True)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE,
                          related_name='muncdata')
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
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    hotline = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:
            now = datetime.datetime.now()
            munc = self.municipality_id
            MuniData.objects.filter(active=True,
                                        municipality_id=munc).update(
                active=False, update_date=now)
            if self.municipality_id.district:
                self.district_id = self.municipality_id.district
            if self.municipality_id.province:
                self.province_id = self.district_id.province

        super().save(*args, **kwargs)


class CovidCases(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE,
                                    related_name='cases', blank=True,
                                    null=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE,
                                    related_name='cases', null=True,
                                    blank=True)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE,
                                        related_name='cases', blank=True,
                                        null=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(default="Male", max_length=15)
    came_from = models.CharField(max_length=255, null=True, blank=True)
    transit = models.CharField(max_length=255, null=True, blank=True)
    labrotary = models.CharField(max_length=255, null=True, blank=True)
    in_isolation = models.BooleanField(default=False)
    current_status = models.CharField(default="unknown",max_length=31)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)
    detected_date = models.DateField(null=True, blank=True)



class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="roles",
                             on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="roles", on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE,
                                 related_name='roles',
                                 blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 related_name='roles',
                                 blank=True, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE,
                                 related_name='roles',
                                 blank=True, null=True)
    facility = models.ForeignKey(MedicalFacility, on_delete=models.CASCADE,
                                 related_name='roles',
                                 blank=True, null=True)


class UserLocation(models.Model):
    update_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="location",
                             on_delete=models.CASCADE)
    location = models.PointField(srid=4326, blank=True, null=True)
    lat = models.FloatField(null=True, blank=True, default=0)
    long = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.location:
            self.lat = self.location.y
            self.long = self.location.x
        elif self.lat and self.long:
            self.location = Point(x=self.long, y=self.lat, srid=4326)
        super(UserLocation, self).save(*args, **kwargs)


class AgeGroupData(models.Model):
    munid = models.IntegerField(default=0)
    provinceId = models.IntegerField(default=0)
    districtId = models.IntegerField(default=0)

    hlcit_code = models.CharField(max_length=63)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE,
                                     related_name='age',
                                     blank=True, null=True)
    pcode = models.CharField(max_length=31)
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 related_name='age', blank=True,
                                 null=True)
    l0_14 = models.IntegerField(default=0)
    l15_49 = models.IntegerField(default=0)
    l50plus = models.IntegerField(default=0)
    ltotal = models.IntegerField(default=0)


class UserReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="report",
                             blank=True, null=True, on_delete=models.SET_NULL)
    device_id = models.CharField(max_length=63, blank=True, null=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    gender = models.CharField(default="Male", max_length=63)
    temperature = models.FloatField(default=0.0)
    in_self_quarrantine = models.BooleanField(default=True)
    have_cough = models.BooleanField(default=True)
    have_fatigue = models.BooleanField(default=True)
    have_throat_pain = models.BooleanField(default=True)
    fast_breathe = models.BooleanField(default=True)
    body_pain = models.BooleanField(default=True)
    diarrahoe = models.BooleanField(default=True)
    vomit = models.BooleanField(default=True)
    runny_nose = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
    symptoms = models.TextField(max_length=255)
    travel_history = models.TextField(max_length=255)
    has_convid_contact = models.BooleanField(default=False)
    has_travel_history = models.BooleanField(default=False)
    location = models.PointField(srid=4326, blank=True, null=True)
    lat = models.FloatField(null=True, blank=True, default=0)
    long = models.FloatField(null=True, blank=True, default=0)
    update_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.location:
            self.lat = self.location.y
            self.long = self.location.x
        elif self.lat and self.long:
            self.location = Point(x=self.long, y=self.lat, srid=4326)
        travel_history = self.travel_history
        try:
            data = json.loads(travel_history)
        except Exception:
            data = {}
        has_travel_history = data.get('has_travel_history', False)
        has_convid_contact = data.get('has_convid_contact', False)
        self.has_convid_contact = has_convid_contact
        self.has_travel_history = has_travel_history
        super(UserReport, self).save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class GlobalData(models.Model):
    total_infected_global = models.IntegerField(default=0)
    total_recovered_global = models.IntegerField(default=0)
    total_deaths_global = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
