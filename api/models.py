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


class MedicalFacility(models.Model):
    # types = (
    #     ('ongoing', 'Ongoing'),
    #     ('completed', 'Completed'),
    #
    # )

    type = models.ForeignKey(MedicalFacilityType, on_delete=models.CASCADE, related_name='Type')
    name = models.CharField(max_length=500, null=True, blank=True)
    ownership = models.CharField(max_length=300, null=True, blank=True)
    contact_num = models.CharField(max_length=500, null=True, blank=True)
    is_used_for_Corona_response = models.CharField(max_length=500, null=True, blank=True)
    num_of_bed = models.IntegerField(null=True, blank=True, default=0)
    num_of_icu_ward = models.IntegerField(null=True, blank=True, default=0)
    num_of_ventilators = models.IntegerField(null=True, blank=True, default=0)
    num_of_isolation_ward = models.IntegerField(null=True, blank=True, default=0)
    remaining_capacity = models.IntegerField(null=True, blank=True, default=0)
    remarks = models.TextField(blank=True)
    lat = models.FloatField(null=True, blank=True, default=0)
    long = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class CovidCases(models.Model):
    total_tested = models.IntegerField(null=True, blank=True, default=0)
    tested_positive = models.IntegerField(null=True, blank=True, default=0)
    tested_negative = models.IntegerField(null=True, blank=True, default=0)
    death = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateField(null=True, blank=True)
