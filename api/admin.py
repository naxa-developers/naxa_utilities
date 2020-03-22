from django.contrib import admin
from .models import MedicalFacility, MedicalFacilityCategory, MedicalFacilityType

# Register your models here.
admin.site.register(MedicalFacility)
admin.site.register(MedicalFacilityCategory)
admin.site.register(MedicalFacilityType)
