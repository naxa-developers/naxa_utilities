from django.db.models import Sum
from .serializers import MedicalFacilitySerializer, \
    MedicalFacilityCategorySerializer, MedicalFacilityTypeSerializer, \
    CaseSerializer, ProvinceSerializer, ProvinceDataSerializer, \
    DistrictSerializer, MunicipalitySerializer, UserRoleSerializer, \
    UserLocationSerializer, UserReportSerializer, AgeGroupDataSerializer, \
    SpaceSerializer
from .models import MedicalFacility, MedicalFacilityType, \
    MedicalFacilityCategory, CovidCases, Province, ProvinceData, Municipality, \
    District, UserLocation, UserReport, AgeGroupData
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, pagination, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

import io
import json
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D
from django.core.serializers import serialize
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

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

NationalHotine = "9851255834, 9851255837, 9851255839 :8 AM – 8 PM: 1115:(6 AM – 10 PM)"


# Create your views here.
class StatsAPI(viewsets.ModelViewSet):
    queryset = ProvinceData.objects.all()
    serializer_class = ProvinceDataSerializer
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
        facility_count = 0
        if province == "all":
            data = ProvinceDataSerializer(queryset, many=True).data
            return Response(data)

        if province:
            queryset = queryset.filter(province_id=province)
            facility_count = MedicalFacility.objects.filter(
                province=province).count()
        else:
            province = "0"
            facility_count = MedicalFacility.objects.all().count()
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
        data.update({'facility_count': facility_count})
        data.update({"hotline": NationalHotine})
        return Response(data)


class MedicalApi(viewsets.ModelViewSet):
    queryset = MedicalFacility.objects.all()
    serializer_class = MedicalFacilitySerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'type', 'municipality', 'district', 'province',
                        'category']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.queryset.select_related('type', 'municipality',
                                            'district', 'province', 'category')


class MedicalApi2(viewsets.ModelViewSet):
    queryset = MedicalFacility.objects.all()
    serializer_class = MedicalFacilitySerializer
    pagination_class = StandardResultsSetPagination

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


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        roles = user.roles.all().select_related("group", "province", "facility")
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'roles': UserRoleSerializer(roles, many=True).data
        })


class UserLocationApi(viewsets.ModelViewSet):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserReportApi(viewsets.ModelViewSet):
    queryset = UserReport.objects.all()
    serializer_class = UserReportSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(user=self.request.user)
        else:
            serializer.save()



class AgeGroupDataApi(viewsets.ModelViewSet):
    queryset = AgeGroupData.objects.all()
    serializer_class = AgeGroupDataSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class NearFacilityViewSet(views.APIView):
    permission_classes = []

    def get(self, request):
        params = request.query_params
        longitude = params['long']
        latitude = params['lat']

        user_location = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=4326)

        resource_queryset = MedicalFacility.objects.filter(
            location__distance_lte=(user_location, D(km=500))).annotate(
            distance=Distance(
                'location', user_location)).order_by('distance')[:10]
        resource_json = SpaceSerializer(resource_queryset, many=True)
        json_data = JSONRenderer().render(resource_json.data)
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        return Response(data)


class SpaceGeojsonViewSet(views.APIView):
    permission_classes = []

    def get(self, request):
        serializers = serialize(
            'geojson', MedicalFacility.objects.all(),
            geometry_field='location', fields=('pk', 'name', 'location',
                                               'province', 'district', 
                                               'municipality', 'category', 
                                               'type', 'ownership', 
                                               'contact_person', 
                                               'contact_num', 
                                               'used_for_corona_response', 
                                               'num_of_bed', 
                                               'num_of_icu_bed', 
                                               'occupied_isolation_bed', 
                                               'occupied_ventilators', 
                                               'occupied_icu_bed',
                                               'num_of_isolation_bed',
                                               'num_of_ventilators',
                                               'total_in_isolation', 
                                               'total_death', 
                                               'total_positive','total_tested'))
        geojson = json.loads(serializers)
        return Response(geojson)