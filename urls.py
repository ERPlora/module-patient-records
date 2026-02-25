from django.urls import path
from . import views

app_name = 'patient_records'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('patients/', views.patient_records_list, name='patients'),
    path('records/', views.dashboard, name='records'),


    # PatientRecord
    path('patient_records/', views.patient_records_list, name='patient_records_list'),
    path('patient_records/add/', views.patient_record_add, name='patient_record_add'),
    path('patient_records/<uuid:pk>/edit/', views.patient_record_edit, name='patient_record_edit'),
    path('patient_records/<uuid:pk>/delete/', views.patient_record_delete, name='patient_record_delete'),
    path('patient_records/<uuid:pk>/toggle/', views.patient_record_toggle_status, name='patient_record_toggle_status'),
    path('patient_records/bulk/', views.patient_records_bulk_action, name='patient_records_bulk_action'),

    # Treatment
    path('treatments/', views.treatments_list, name='treatments_list'),
    path('treatments/add/', views.treatment_add, name='treatment_add'),
    path('treatments/<uuid:pk>/edit/', views.treatment_edit, name='treatment_edit'),
    path('treatments/<uuid:pk>/delete/', views.treatment_delete, name='treatment_delete'),
    path('treatments/bulk/', views.treatments_bulk_action, name='treatments_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
