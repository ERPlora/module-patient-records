from django.utils.translation import gettext_lazy as _

MODULE_ID = 'patient_records'
MODULE_NAME = _('Patient Records')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'medical-outline'
MODULE_DESCRIPTION = _('Patient medical records, treatments and prescriptions')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'specialized'

MENU = {
    'label': _('Patient Records'),
    'icon': 'medical-outline',
    'order': 90,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Patients'), 'icon': 'medical-outline', 'id': 'patients'},
{'label': _('Records'), 'icon': 'document-text-outline', 'id': 'records'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'patient_records.view_patientrecord',
'patient_records.add_patientrecord',
'patient_records.change_patientrecord',
'patient_records.view_treatment',
'patient_records.add_treatment',
'patient_records.change_treatment',
'patient_records.manage_settings',
]
