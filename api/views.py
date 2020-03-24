from django.db.models import Sum
from django.shortcuts import render
from rest_framework import viewsets, views
from .serializers import MedicalFacilitySerializer, \
    MedicalFacilityCategorySerializer, MedicalFacilityTypeSerializer, \
    CaseSerializer, ProvinceSerializer, ProvinceDataSerializer, \
    DistrictSerializer, MunicipalitySerializer
from .models import MedicalFacility, MedicalFacilityType, \
    MedicalFacilityCategory, CovidCases, Province, ProvinceData, Municipality, \
    District
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.response import Response

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


# Create your views here.
class StatsAPI(viewsets.ModelViewSet):
    queryset = ProvinceData.objects.all()
    serializer_class = ProvinceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'province_id']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = ProvinceData.objects.filter(active=True)
        province = self.request.query_params.get('province')
        if province:
            queryset = queryset.filter(province_id=province)
        else:
            province = "0"
        hotline = HOTLINES.get(province, {})
        data = queryset.aggregate(
            tested=Sum('total_tested'),
            confirmed=Sum('total_positive'),
            isolation=Sum('total_in_isolation'),
            death=Sum('total_death'),
            icu=Sum('num_of_icu_bed'),
            occupied_icu=Sum('occupied_icu_bed'),
            ventilator=Sum('num_of_ventilators'),
            occupied_ventilator=Sum('occupied_ventilators'),
            isolation_bed=Sum('num_of_isolation_bed'),
            occupied_isolation_bed=Sum('occupied_ventilators'),
        )
        data.update(hotline)
        return Response(data)


class MedicalApi(viewsets.ModelViewSet):
    queryset = MedicalFacility.objects.all()
    serializer_class = MedicalFacilitySerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'type']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class MedicalCategoryApi(viewsets.ModelViewSet):
    queryset = MedicalFacilityCategory.objects.order_by('id')
    serializer_class = MedicalFacilityCategorySerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class MedicalTypeApi(viewsets.ModelViewSet):
    queryset = MedicalFacilityType.objects.order_by('id')
    serializer_class = MedicalFacilityTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class CaseApi(viewsets.ModelViewSet):
    queryset = CovidCases.objects.order_by('id')
    serializer_class = CaseSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ProvinceApi(viewsets.ModelViewSet):
    queryset = Province.objects.order_by('id')
    serializer_class = ProvinceSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class MunicipalityApi(viewsets.ModelViewSet):
    queryset = Municipality.objects.order_by('id')
    serializer_class = MunicipalitySerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class DistrictApi(viewsets.ModelViewSet):
    queryset = District.objects.order_by('id')
    serializer_class = DistrictSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ProvinceDataApi(viewsets.ModelViewSet):
    queryset = ProvinceData.objects.order_by('id')
    serializer_class = ProvinceDataSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
