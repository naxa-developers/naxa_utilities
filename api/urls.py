from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

from api.views import NearFacilityViewSet, SpaceGeojsonViewSet

router = DefaultRouter()
router.register(r'province', views.ProvinceApi)
router.register(r'district', views.DistrictApi)
router.register(r'municipality', views.MunicipalityApi)
# router.register(r'province-data', views.ProvinceDataApi)
router.register(r'positive-cases', views.CaseApi)
router.register(r'global-data', views.GlobalDataApi)
router.register(r'mobile-version', views.VersionDataApi)
router.register(r'health-type', views.MedicalTypeApi)
router.register(r'health-category', views.MedicalCategoryApi) # left bar
router.register(r'health-facility', views.MedicalApi)
router.register(r'health-facility2', views.MedicalApi2)
router.register(r'track-me', views.UserLocationApi)
router.register(r'user-report', views.UserReportApi)
router.register(r'age-data', views.AgeGroupDataApi)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.StatsAPI.as_view(
        {'get': 'list'})),
    path('near-facility/', NearFacilityViewSet.as_view(), name="api"),
    path('geojson/facility/', SpaceGeojsonViewSet.as_view(), name="space"),
]

urlpatterns += [
    path('api-token-auth/', views.CustomAuthToken.as_view())
]
