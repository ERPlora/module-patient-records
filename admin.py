from django.contrib import admin

from .models import PatientRecord, Treatment

@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'date_of_birth', 'gender', 'blood_type', 'allergies']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'description', 'diagnosis', 'prescription']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

