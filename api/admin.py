from django.contrib import admin
from .models import MedicalFacility, MedicalFacilityCategory, MedicalFacilityType, CovidCases, Province, ProvinceData

# Register your models here.
admin.site.register(MedicalFacility)
admin.site.register(MedicalFacilityCategory)
admin.site.register(MedicalFacilityType)
admin.site.register(Province)


class ProvinceDataAdmin(admin.ModelAdmin):
    list_filter = ('province_id', 'date')
    list_display = ('province_id', 'date')
    search_fields = ('province_id', 'date')


class CovidCasesAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    list_display = ('death', 'date')
    search_fields = ('date',)


admin.site.register(ProvinceData, ProvinceDataAdmin)
admin.site.register(CovidCases, CovidCasesAdmin)
