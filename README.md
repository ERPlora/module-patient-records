# Patient Records

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `patient_records` |
| **Version** | `1.0.0` |
| **Icon** | `medical-outline` |
| **Dependencies** | None |

## Models

### `PatientRecord`

PatientRecord(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, patient_name, date_of_birth, gender, blood_type, allergies, medical_notes, is_active)

| Field | Type | Details |
|-------|------|---------|
| `patient_name` | CharField | max_length=255 |
| `date_of_birth` | DateField | optional |
| `gender` | CharField | max_length=20, optional |
| `blood_type` | CharField | max_length=5, optional |
| `allergies` | TextField | optional |
| `medical_notes` | TextField | optional |
| `is_active` | BooleanField |  |

### `Treatment`

Treatment(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, patient, date, description, diagnosis, prescription, practitioner_id, notes)

| Field | Type | Details |
|-------|------|---------|
| `patient` | ForeignKey | → `patient_records.PatientRecord`, on_delete=CASCADE |
| `date` | DateField |  |
| `description` | TextField |  |
| `diagnosis` | TextField | optional |
| `prescription` | TextField | optional |
| `practitioner_id` | UUIDField | max_length=32, optional |
| `notes` | TextField | optional |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `Treatment` | `patient` | `patient_records.PatientRecord` | CASCADE | No |

## URL Endpoints

Base path: `/m/patient_records/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `patients/` | `patients` | GET |
| `records/` | `records` | GET |
| `patient_records/` | `patient_records_list` | GET |
| `patient_records/add/` | `patient_record_add` | GET/POST |
| `patient_records/<uuid:pk>/edit/` | `patient_record_edit` | GET |
| `patient_records/<uuid:pk>/delete/` | `patient_record_delete` | GET/POST |
| `patient_records/<uuid:pk>/toggle/` | `patient_record_toggle_status` | GET |
| `patient_records/bulk/` | `patient_records_bulk_action` | GET/POST |
| `treatments/` | `treatments_list` | GET |
| `treatments/add/` | `treatment_add` | GET/POST |
| `treatments/<uuid:pk>/edit/` | `treatment_edit` | GET |
| `treatments/<uuid:pk>/delete/` | `treatment_delete` | GET/POST |
| `treatments/bulk/` | `treatments_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `patient_records.view_patientrecord` | View Patientrecord |
| `patient_records.add_patientrecord` | Add Patientrecord |
| `patient_records.change_patientrecord` | Change Patientrecord |
| `patient_records.view_treatment` | View Treatment |
| `patient_records.add_treatment` | Add Treatment |
| `patient_records.change_treatment` | Change Treatment |
| `patient_records.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_patientrecord`, `add_treatment`, `change_patientrecord`, `change_treatment`, `view_patientrecord`, `view_treatment`
- **employee**: `add_patientrecord`, `view_patientrecord`, `view_treatment`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Patients | `medical-outline` | `patients` | No |
| Records | `document-text-outline` | `records` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_patients`

List patient records.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_active` | boolean | No |  |
| `search` | string | No |  |
| `limit` | integer | No |  |

### `create_patient`

Create a patient record.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `patient_name` | string | Yes |  |
| `date_of_birth` | string | No |  |
| `gender` | string | No |  |
| `blood_type` | string | No |  |
| `allergies` | string | No |  |
| `medical_notes` | string | No |  |

### `list_treatments`

List patient treatments.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `patient_id` | string | No |  |
| `limit` | integer | No |  |

### `create_treatment`

Create a treatment record for a patient.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `patient_id` | string | Yes |  |
| `date` | string | Yes |  |
| `description` | string | Yes |  |
| `diagnosis` | string | No |  |
| `prescription` | string | No |  |
| `notes` | string | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  patient_records/
    css/
    js/
templates/
  patient_records/
    pages/
      dashboard.html
      index.html
      patient_record_add.html
      patient_record_edit.html
      patient_records.html
      patients.html
      records.html
      settings.html
      treatment_add.html
      treatment_edit.html
      treatments.html
    partials/
      dashboard_content.html
      panel_patient_record_add.html
      panel_patient_record_edit.html
      panel_treatment_add.html
      panel_treatment_edit.html
      patient_record_add_content.html
      patient_record_edit_content.html
      patient_records_content.html
      patient_records_list.html
      patients_content.html
      records_content.html
      settings_content.html
      treatment_add_content.html
      treatment_edit_content.html
      treatments_content.html
      treatments_list.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
