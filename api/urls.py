from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'province', views.ProvinceApi)
router.register(r'province-data', views.ProvinceDataApi)
router.register(r'cases', views.CaseApi)
router.register(r'health-type', views.MedicalTypeApi)
router.register(r'health-category', views.MedicalCategoryApi)
router.register(r'health-facility', views.MedicalApi)

urlpatterns = [
    path('', include(router.urls)),
    # path('health-facility/', views.MedicalApi.as_view({'get': 'list'}), name='health-facility'),
    # path('health-category/', views.MedicalCategoryApi.as_view({'get': 'list'}), name='health-category'),
    # path('health-type/', views.MedicalTypeApi.as_view({'get': 'list'}), name='health-type'),
    # path('cases/', views.CaseApi.as_view({'get': 'list'}), name='cases'),
    # path('province-data/', views.ProvinceDataApi.as_view({'get': 'list'}), name='province-data'),
]
