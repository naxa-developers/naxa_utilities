from django.shortcuts import render
from rest_framework import viewsets, views
from .serializers import MedicalFacilitySerializer, MedicalFacilityCategorySerializer, MedicalFacilityTypeSerializer
from .models import MedicalFacility, MedicalFacilityType, MedicalFacilityCategory
from rest_framework.permissions import AllowAny, IsAuthenticated


# Create your views here.

class MedicalApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id']

    def get_queryset(self):
        queryset = MedicalFacility.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MedicalFacilitySerializer
        return serializer_class


class MedicalCategoryApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id']

    def get_queryset(self):
        queryset = MedicalFacilityCategory.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MedicalFacilityCategorySerializer
        return serializer_class


class MedicalTypeApi(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id']

    def get_queryset(self):
        queryset = MedicalFacilityType.objects.order_by('id')
        return queryset

    def get_serializer_class(self):
        serializer_class = MedicalFacilityTypeSerializer
        return serializer_class
