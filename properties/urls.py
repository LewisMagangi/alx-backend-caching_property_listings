from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('api/', views.property_list_json, name='property_list_json'),
]
