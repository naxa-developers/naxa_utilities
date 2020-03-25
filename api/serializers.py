from rest_framework import serializers
from .models import MedicalFacility, MedicalFacilityCategory, \
    MedicalFacilityType, CovidCases, Province, ProvinceData, District, \
    Municipality

HOTLINES = {"0": {"phones" :["11111111", "22222222", "2222222"],
                             'time': "9am - 6 PM"},
            "1": {"phones" :["11111111", "22222222", "2222222"],
                             'time': "9am - 6 PM"},
            "2": {"phones" :["11111111", "22222222", "2222222"],
                             'time': "9am - 6 PM"},
            "3": {"phones" :["11111111", "22222222", "2222222"],
                             'time': "9am - 6 PM"},
            "4": {"phones" :["11111111", "22222222", "2222222"],
                             'time': "9am - 6 PM"},
            "5": {"phones" :["11111111", "22222222", "2222222"],
                             'time': "9am - 6 PM"},
            "6": {"phones" :["11111111", "22222222", "2222222"],
                             'time': "9am - 6 PM"},
            "7": {"phones" :["11111111", "22222222", "2222222"],
                             'time': "9am - 6 PM"},
            }



class MedicalFacilityCategorySerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = MedicalFacilityCategory
        fields = ('id', 'name', 'type')

    def get_type(self, obj):
        qs = obj.Category.all().order_by('id').values('id', 'name')
        return qs


class MedicalFacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFacilityType
        fields = "__all__"


class MedicalFacilitySerializer(serializers.ModelSerializer):
    ownership_display = serializers.CharField(source="get_ownership_display",
                                           read_only=True)
    class Meta:
        model = MedicalFacility
        # fields = ('name', 'id', 'num_of_bed', 'contact_num', 'is_used_for_Corona_response', 'num_of_icu_ward',
        #           'num_of_ventilators', 'num_of_isolation_ward', 'remaining_capacity', 'remarks', 'lat',)
        fields = "__all__"


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidCases
        fields = "__all__"


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = "__all__"


class ProvinceDataSerializer(serializers.ModelSerializer):
    phones = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = ProvinceData
        fields = "__all__"

    def get_phones(self, obj):
        return HOTLINES[str(obj.id)]['phones']

    def get_time(self, obj):
        return HOTLINES[str(obj.id)]['time']
