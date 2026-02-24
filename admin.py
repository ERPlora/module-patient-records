from django.contrib import admin

from .models import PatientRecord, Treatment

@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'date_of_birth', 'gender', 'blood_type', 'created_at']
    search_fields = ['patient_name', 'gender', 'blood_type', 'allergies']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'created_at']
    search_fields = ['description', 'diagnosis', 'prescription', 'notes']
    readonly_fields = ['created_at', 'updated_at']

