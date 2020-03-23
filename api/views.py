from django.shortcuts import render
from rest_framework import viewsets, views
from .serializers import MedicalFacilitySerializer, MedicalFacilityCategorySerializer, MedicalFacilityTypeSerializer, \
    CaseSerializer, ProvinceSerializer, ProvinceDataSerializer
from .models import MedicalFacility, MedicalFacilityType, MedicalFacilityCategory, CovidCases, Province, ProvinceData
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class MedicalApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'type']

    def get_queryset(self):
        queryset = MedicalFacility.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MedicalFacilitySerializer
        return serializer_class


class MedicalCategoryApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = MedicalFacilityCategory.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MedicalFacilityCategorySerializer
        return serializer_class


class MedicalTypeApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category']

    def get_queryset(self):
        queryset = MedicalFacilityType.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MedicalFacilityTypeSerializer
        return serializer_class


class CaseApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', ]

    def get_queryset(self):
        queryset = CovidCases.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = CaseSerializer
        return serializer_class


class ProvinceApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', ]

    def get_queryset(self):
        queryset = Province.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProvinceSerializer
        return serializer_class


class ProvinceDataApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', ]

    def get_queryset(self):
        queryset = ProvinceData.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = ProvinceDataSerializer
        return serializer_class
