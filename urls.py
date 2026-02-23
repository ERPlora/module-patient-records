from django.urls import path
from . import views

app_name = 'patient_records'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.patients, name='patients'),
    path('records/', views.records, name='records'),
    path('settings/', views.settings, name='settings'),
]
