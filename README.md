# Patient Records Module

Patient medical records, treatments and prescriptions management.

## Features

- Patient records with personal and medical information
- Track date of birth, gender, blood type, and allergies
- Medical notes and active/inactive patient status
- Treatment records linked to patients with date, description, and diagnosis
- Prescription tracking per treatment
- Practitioner assignment via UUID reference
- Treatment-level notes for additional clinical observations

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Patient Records > Settings**

## Usage

Access via: **Menu > Patient Records**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/patient_records/dashboard/` | Overview of patient and treatment activity |
| Patients | `/m/patient_records/patients/` | Manage patient records and medical information |
| Records | `/m/patient_records/records/` | View and manage treatment records |
| Settings | `/m/patient_records/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `PatientRecord` | Patient profile with name, date of birth, gender, blood type, allergies, medical notes, and active status |
| `Treatment` | Treatment entry linked to a patient with date, description, diagnosis, prescription, practitioner reference, and notes |

## Permissions

| Permission | Description |
|------------|-------------|
| `patient_records.view_patientrecord` | View patient records |
| `patient_records.add_patientrecord` | Create new patient records |
| `patient_records.change_patientrecord` | Edit patient records |
| `patient_records.view_treatment` | View treatment records |
| `patient_records.add_treatment` | Create new treatment entries |
| `patient_records.change_treatment` | Edit treatment entries |
| `patient_records.manage_settings` | Access and modify module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
