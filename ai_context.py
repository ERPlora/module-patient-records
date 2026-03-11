"""
AI context for the Patient Records module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Patient Records

### Models

**PatientRecord** — core patient demographic and medical data.
- `patient_name` (str): full name
- `date_of_birth` (date, nullable)
- `gender` (str, max 20): free text (e.g. "male", "female", "other")
- `blood_type` (str, max 5): e.g. "A+", "O-", "AB+"
- `allergies` (text): known allergies list
- `medical_notes` (text): general medical history and notes
- `is_active` (bool, default True): inactive = discharged or archived

**Treatment** — a clinical encounter or treatment session linked to a patient.
- `patient` (FK → PatientRecord): the patient treated
- `date` (date): date of the treatment/visit
- `description` (text): what was done (procedures, services performed)
- `diagnosis` (text): clinical diagnosis
- `prescription` (text): medications or therapies prescribed
- `practitioner_id` (UUID, nullable): ID of the treating professional (references accounts.LocalUser)
- `notes` (text): additional clinical notes

### Key flows

1. **Register a patient**: create PatientRecord with name and demographic info.
2. **Record a visit**: create Treatment linked to the patient with date, description, diagnosis, and prescription.
3. **View patient history**: query Treatment.objects.filter(patient=patient).order_by('-date').
4. **Archive a patient**: set PatientRecord.is_active=False.
5. **Search patients**: filter PatientRecord by patient_name (icontains) or filter by is_active=True.

### Relationships
- Treatment.patient → PatientRecord
- Treatment.practitioner_id → UUID reference to accounts.LocalUser (no FK constraint)

### Notes
- This module contains sensitive health data — handle with appropriate confidentiality.
- blood_type valid values: A+, A-, B+, B-, AB+, AB-, O+, O-.
"""
