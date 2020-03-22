from django.contrib.gis.db import models


class MedicalFacilityCategory(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)


class MedicalFacilitySubCategory(models.Model):
    category = models.ForeignKey(MedicalFacilityCategory, on_delete=models.CASCADE, related_name='Category')
    name = models.CharField(max_length=500, null=True, blank=True)


class MedicalFacility(models.Model):
    sub_category = models.ForeignKey(MedicalFacilitySubCategory, on_delete=models.CASCADE, related_name='Subcategory')
    name = models.CharField(max_length=500, null=True, blank=True)
