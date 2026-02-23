from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatientRecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patient_records'
    label = 'patient_records'
    verbose_name = _('Patient Records')

    def ready(self):
        pass
