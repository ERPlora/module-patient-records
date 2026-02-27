"""
Patient Records Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import PatientRecord, Treatment

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('patient_records', 'dashboard')
@htmx_view('patient_records/pages/index.html', 'patient_records/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_patient_records': PatientRecord.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_treatments': Treatment.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# PatientRecord
# ======================================================================

PATIENT_RECORD_SORT_FIELDS = {
    'is_active': 'is_active',
    'patient_name': 'patient_name',
    'date_of_birth': 'date_of_birth',
    'gender': 'gender',
    'blood_type': 'blood_type',
    'allergies': 'allergies',
    'created_at': 'created_at',
}

def _build_patient_records_context(hub_id, per_page=10):
    qs = PatientRecord.objects.filter(hub_id=hub_id, is_deleted=False).order_by('is_active')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'patient_records': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'is_active',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_patient_records_list(request, hub_id, per_page=10):
    ctx = _build_patient_records_context(hub_id, per_page)
    return django_render(request, 'patient_records/partials/patient_records_list.html', ctx)

@login_required
@with_module_nav('patient_records', 'patients')
@htmx_view('patient_records/pages/patient_records.html', 'patient_records/partials/patient_records_content.html')
def patient_records_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'is_active')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = PatientRecord.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(patient_name__icontains=search_query) | Q(gender__icontains=search_query) | Q(blood_type__icontains=search_query) | Q(allergies__icontains=search_query))

    order_by = PATIENT_RECORD_SORT_FIELDS.get(sort_field, 'is_active')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['is_active', 'patient_name', 'date_of_birth', 'gender', 'blood_type', 'allergies']
        headers = ['Is Active', 'Patient Name', 'Date Of Birth', 'Gender', 'Blood Type', 'Allergies']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='patient_records.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='patient_records.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'patient_records/partials/patient_records_list.html', {
            'patient_records': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'patient_records': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def patient_record_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name', '').strip()
        date_of_birth = request.POST.get('date_of_birth') or None
        gender = request.POST.get('gender', '').strip()
        blood_type = request.POST.get('blood_type', '').strip()
        allergies = request.POST.get('allergies', '').strip()
        medical_notes = request.POST.get('medical_notes', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = PatientRecord(hub_id=hub_id)
        obj.patient_name = patient_name
        obj.date_of_birth = date_of_birth
        obj.gender = gender
        obj.blood_type = blood_type
        obj.allergies = allergies
        obj.medical_notes = medical_notes
        obj.is_active = is_active
        obj.save()
        return _render_patient_records_list(request, hub_id)
    return django_render(request, 'patient_records/partials/panel_patient_record_add.html', {})

@login_required
def patient_record_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(PatientRecord, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.patient_name = request.POST.get('patient_name', '').strip()
        obj.date_of_birth = request.POST.get('date_of_birth') or None
        obj.gender = request.POST.get('gender', '').strip()
        obj.blood_type = request.POST.get('blood_type', '').strip()
        obj.allergies = request.POST.get('allergies', '').strip()
        obj.medical_notes = request.POST.get('medical_notes', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_patient_records_list(request, hub_id)
    return django_render(request, 'patient_records/partials/panel_patient_record_edit.html', {'obj': obj})

@login_required
@require_POST
def patient_record_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(PatientRecord, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_patient_records_list(request, hub_id)

@login_required
@require_POST
def patient_record_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(PatientRecord, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_patient_records_list(request, hub_id)

@login_required
@require_POST
def patient_records_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = PatientRecord.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_patient_records_list(request, hub_id)


# ======================================================================
# Treatment
# ======================================================================

TREATMENT_SORT_FIELDS = {
    'patient': 'patient',
    'date': 'date',
    'description': 'description',
    'diagnosis': 'diagnosis',
    'prescription': 'prescription',
    'practitioner_id': 'practitioner_id',
    'created_at': 'created_at',
}

def _build_treatments_context(hub_id, per_page=10):
    qs = Treatment.objects.filter(hub_id=hub_id, is_deleted=False).order_by('patient')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'treatments': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'patient',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_treatments_list(request, hub_id, per_page=10):
    ctx = _build_treatments_context(hub_id, per_page)
    return django_render(request, 'patient_records/partials/treatments_list.html', ctx)

@login_required
@with_module_nav('patient_records', 'patients')
@htmx_view('patient_records/pages/treatments.html', 'patient_records/partials/treatments_content.html')
def treatments_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'patient')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Treatment.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(description__icontains=search_query) | Q(diagnosis__icontains=search_query) | Q(prescription__icontains=search_query) | Q(notes__icontains=search_query))

    order_by = TREATMENT_SORT_FIELDS.get(sort_field, 'patient')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['patient', 'date', 'description', 'diagnosis', 'prescription', 'practitioner_id']
        headers = ['PatientRecord', 'Date', 'Description', 'Diagnosis', 'Prescription', 'Practitioner Id']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='treatments.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='treatments.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'patient_records/partials/treatments_list.html', {
            'treatments': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'treatments': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def treatment_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        date = request.POST.get('date') or None
        description = request.POST.get('description', '').strip()
        diagnosis = request.POST.get('diagnosis', '').strip()
        prescription = request.POST.get('prescription', '').strip()
        practitioner_id = request.POST.get('practitioner_id', '').strip()
        notes = request.POST.get('notes', '').strip()
        obj = Treatment(hub_id=hub_id)
        obj.date = date
        obj.description = description
        obj.diagnosis = diagnosis
        obj.prescription = prescription
        obj.practitioner_id = practitioner_id
        obj.notes = notes
        obj.save()
        return _render_treatments_list(request, hub_id)
    return django_render(request, 'patient_records/partials/panel_treatment_add.html', {})

@login_required
def treatment_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Treatment, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.date = request.POST.get('date') or None
        obj.description = request.POST.get('description', '').strip()
        obj.diagnosis = request.POST.get('diagnosis', '').strip()
        obj.prescription = request.POST.get('prescription', '').strip()
        obj.practitioner_id = request.POST.get('practitioner_id', '').strip()
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_treatments_list(request, hub_id)
    return django_render(request, 'patient_records/partials/panel_treatment_edit.html', {'obj': obj})

@login_required
@require_POST
def treatment_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Treatment, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_treatments_list(request, hub_id)

@login_required
@require_POST
def treatments_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Treatment.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_treatments_list(request, hub_id)


@login_required
@permission_required('patient_records.manage_settings')
@with_module_nav('patient_records', 'settings')
@htmx_view('patient_records/pages/settings.html', 'patient_records/partials/settings_content.html')
def settings_view(request):
    return {}

