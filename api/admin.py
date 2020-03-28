from django.contrib import admin
from .models import MedicalFacility, MedicalFacilityCategory, \
    MedicalFacilityType, Province, ProvinceData, UserRole, \
    Municipality, District, UserLocation, UserReport, DistrictData, MuniData

from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
# admin.site.register(MedicalFacility)
admin.site.register(MedicalFacilityCategory)
admin.site.register(MedicalFacilityType)
admin.site.register(Province)

admin.site.register(Municipality)
admin.site.register(District)

class ProvinceDataAdmin(admin.ModelAdmin):
    list_filter = ('province_id', 'update_date', 'active')
    list_display = ('province_id', 'update_date', 'active')
    search_fields = ('province_id', 'update_date', 'active')


class UserRoleAdmin(admin.ModelAdmin):
    list_filter = ('group', 'province')
    list_display = ('user', 'user__first_name', 'user__last_name', 'group',
                    'active')
    search_fields = ('user', 'active')


class DistrictDataAdmin(admin.ModelAdmin):
    list_filter = ('district_id', 'update_date', 'active')
    list_display = ('district_id', 'update_date', 'active', 'province_id')
    search_fields = ('district_id', 'update_date', 'active')


class MuniDataAdmin(admin.ModelAdmin):
    list_filter = ('municipality_id', 'update_date', 'active')
    list_display = ('municipality_id', 'update_date', 'active', 'province_id')
    search_fields = ('municipality_id', 'update_date', 'active')


class CovidCasesAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    list_display = ('death', 'date')
    search_fields = ('date',)


admin.site.register(ProvinceData, ProvinceDataAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(MuniData, MuniDataAdmin)
admin.site.register(DistrictData, DistrictDataAdmin)


class MarkerAdmin(OSMGeoAdmin):
    default_lon = 84
    default_lat = 28
    default_zoom = 75
    readonly_fields = ('lat', 'long')
    list_filter = ('district', 'province', 'municipality')
    list_display = ('name', 'district', 'province', 'municipality',
                    'num_of_bed', 'num_of_icu_bed', 'occupied_icu_bed',
                    'num_of_ventilators', 'occupied_ventilators',
                    'num_of_isolation_bed', 'occupied_isolation_bed')
    search_fields = ('district', 'province', 'municipality')


admin.site.register(MedicalFacility, MarkerAdmin)


class ReportAdmin(OSMGeoAdmin):
    default_lon = 84
    default_lat = 28
    default_zoom = 100
    readonly_fields = ('lat', 'long')
    list_filter = ('fast_breathe',)
    list_display = ('name', 'temperature', 'fast_breathe')


admin.site.register(UserReport, ReportAdmin)


class UserLocationAdmin(OSMGeoAdmin):
    default_lon = 84
    default_lat = 28
    default_zoom = 50
    readonly_fields = ('lat', 'long')
    list_filter = ('user',)
    list_display = ('user', 'lat', 'long')


admin.site.register(UserLocation, UserLocationAdmin)
