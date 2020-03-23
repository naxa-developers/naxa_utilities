from django.shortcuts import render
from rest_framework import viewsets, views
from .serializers import MedicalFacilitySerializer, MedicalFacilityCategorySerializer, MedicalFacilityTypeSerializer, \
    CaseSerializer, ProvinceSerializer, ProvinceDataSerializer
from .models import MedicalFacility, MedicalFacilityType, MedicalFacilityCategory, CovidCases, Province, ProvinceData
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class MedicalApi(viewsets.ModelViewSet):
    queryset = MedicalFacility.objects.order_by('id')
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
