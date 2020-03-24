from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'province', views.ProvinceApi)
# router.register(r'province-data', views.ProvinceDataApi)
# router.register(r'cases', views.CaseApi)
router.register(r'health-type', views.MedicalTypeApi)
router.register(r'health-category', views.MedicalCategoryApi) # left bar
# router.register(r'health-facility', views.MedicalApi)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/<int:pk>', views.StatsAPI.as_view(
        {'get': 'retrieve', 'put': 'update'})),
    path('stats/', views.StatsAPI.as_view(
        {'get': 'list', 'post': 'create'})),
]
