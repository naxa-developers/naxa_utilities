from django.urls import path, include
from api import views

urlpatterns = [
    path('health-facility/', views.MedicalApi.as_view({'get': 'list'}), name='health-facility'),
    path('health-category/', views.MedicalCategoryApi.as_view({'get': 'list'}), name='health-category'),
    path('health-type/', views.MedicalTypeApi.as_view({'get': 'list'}), name='health-type'),
    path('cases/', views.CaseApi.as_view({'get': 'list'}), name='cases'),
    path('province/', views.ProvinceApi.as_view({'get': 'list'}), name='province'),
    path('province-data/', views.ProvinceDataApi.as_view({'get': 'list'}), name='province-data'),
]
