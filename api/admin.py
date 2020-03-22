from django.contrib import admin
from .models import MedicalFacility, MedicalFacilityCategory, MedicalFacilityType, CovidCases

# Register your models here.
admin.site.register(MedicalFacility)
admin.site.register(MedicalFacilityCategory)
admin.site.register(MedicalFacilityType)
admin.site.register(CovidCases)
