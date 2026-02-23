from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class PatientRecord(HubBaseModel):
    patient_name = models.CharField(max_length=255, verbose_name=_('Patient Name'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date Of Birth'))
    gender = models.CharField(max_length=20, blank=True, verbose_name=_('Gender'))
    blood_type = models.CharField(max_length=5, blank=True, verbose_name=_('Blood Type'))
    allergies = models.TextField(blank=True, verbose_name=_('Allergies'))
    medical_notes = models.TextField(blank=True, verbose_name=_('Medical Notes'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'patient_records_patientrecord'

    def __str__(self):
        return str(self.id)


class Treatment(HubBaseModel):
    patient = models.ForeignKey('PatientRecord', on_delete=models.CASCADE, related_name='treatments')
    date = models.DateField(verbose_name=_('Date'))
    description = models.TextField(verbose_name=_('Description'))
    diagnosis = models.TextField(blank=True, verbose_name=_('Diagnosis'))
    prescription = models.TextField(blank=True, verbose_name=_('Prescription'))
    practitioner_id = models.UUIDField(null=True, blank=True, verbose_name=_('Practitioner Id'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'patient_records_treatment'

    def __str__(self):
        return str(self.id)

