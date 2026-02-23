"""
Patient Records Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('patient_records', 'dashboard')
@htmx_view('patient_records/pages/dashboard.html', 'patient_records/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('patient_records', 'patients')
@htmx_view('patient_records/pages/patients.html', 'patient_records/partials/patients_content.html')
def patients(request):
    """Patients view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('patient_records', 'records')
@htmx_view('patient_records/pages/records.html', 'patient_records/partials/records_content.html')
def records(request):
    """Records view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('patient_records', 'settings')
@htmx_view('patient_records/pages/settings.html', 'patient_records/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

