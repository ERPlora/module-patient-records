"""AI tools for the Patient Records module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListPatients(AssistantTool):
    name = "list_patients"
    description = "List patient records."
    module_id = "patient_records"
    required_permission = "patient_records.view_patientrecord"
    parameters = {
        "type": "object",
        "properties": {"is_active": {"type": "boolean"}, "search": {"type": "string"}, "limit": {"type": "integer"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from patient_records.models import PatientRecord
        qs = PatientRecord.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        if args.get('search'):
            qs = qs.filter(patient_name__icontains=args['search'])
        limit = args.get('limit', 20)
        return {"patients": [{"id": str(p.id), "patient_name": p.patient_name, "date_of_birth": str(p.date_of_birth) if p.date_of_birth else None, "gender": p.gender, "blood_type": p.blood_type, "allergies": p.allergies, "is_active": p.is_active} for p in qs[:limit]]}


@register_tool
class CreatePatient(AssistantTool):
    name = "create_patient"
    description = "Create a patient record."
    module_id = "patient_records"
    required_permission = "patient_records.add_patientrecord"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "patient_name": {"type": "string"}, "date_of_birth": {"type": "string"},
            "gender": {"type": "string"}, "blood_type": {"type": "string"},
            "allergies": {"type": "string"}, "medical_notes": {"type": "string"},
        },
        "required": ["patient_name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from patient_records.models import PatientRecord
        p = PatientRecord.objects.create(
            patient_name=args['patient_name'], date_of_birth=args.get('date_of_birth'),
            gender=args.get('gender', ''), blood_type=args.get('blood_type', ''),
            allergies=args.get('allergies', ''), medical_notes=args.get('medical_notes', ''),
        )
        return {"id": str(p.id), "patient_name": p.patient_name, "created": True}


@register_tool
class ListTreatments(AssistantTool):
    name = "list_treatments"
    description = "List patient treatments."
    module_id = "patient_records"
    required_permission = "patient_records.view_treatment"
    parameters = {
        "type": "object",
        "properties": {"patient_id": {"type": "string"}, "limit": {"type": "integer"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from patient_records.models import Treatment
        qs = Treatment.objects.select_related('patient').all()
        if args.get('patient_id'):
            qs = qs.filter(patient_id=args['patient_id'])
        limit = args.get('limit', 20)
        return {"treatments": [{"id": str(t.id), "patient": t.patient.patient_name, "date": str(t.date), "description": t.description, "diagnosis": t.diagnosis, "prescription": t.prescription} for t in qs.order_by('-date')[:limit]]}


@register_tool
class CreateTreatment(AssistantTool):
    name = "create_treatment"
    description = "Create a treatment record for a patient."
    module_id = "patient_records"
    required_permission = "patient_records.add_treatment"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "patient_id": {"type": "string"}, "date": {"type": "string"},
            "description": {"type": "string"}, "diagnosis": {"type": "string"},
            "prescription": {"type": "string"}, "notes": {"type": "string"},
        },
        "required": ["patient_id", "date", "description"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from patient_records.models import Treatment
        t = Treatment.objects.create(
            patient_id=args['patient_id'], date=args['date'], description=args['description'],
            diagnosis=args.get('diagnosis', ''), prescription=args.get('prescription', ''),
            notes=args.get('notes', ''),
        )
        return {"id": str(t.id), "created": True}


@register_tool
class DeletePatient(AssistantTool):
    name = "delete_patient"
    description = "Deactivate (soft-delete) a patient record."
    module_id = "patient_records"
    required_permission = "patient_records.change_patientrecord"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"patient_id": {"type": "string"}},
        "required": ["patient_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from patient_records.models import PatientRecord
        try:
            p = PatientRecord.objects.get(id=args['patient_id'])
            p.is_active = False
            p.save(update_fields=['is_active', 'updated_at'])
            return {"deactivated": True, "patient_name": p.patient_name}
        except PatientRecord.DoesNotExist:
            return {"error": "Patient not found"}


@register_tool
class UpdatePatientVisit(AssistantTool):
    name = "update_patient_visit"
    description = "Update a patient treatment/visit record."
    module_id = "patient_records"
    required_permission = "patient_records.change_treatment"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "treatment_id": {"type": "string"},
            "date": {"type": "string"},
            "description": {"type": "string"},
            "diagnosis": {"type": "string"},
            "prescription": {"type": "string"},
            "notes": {"type": "string"},
        },
        "required": ["treatment_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from patient_records.models import Treatment
        try:
            t = Treatment.objects.get(id=args['treatment_id'])
        except Treatment.DoesNotExist:
            return {"error": "Treatment not found"}
        fields = []
        for field in ('date', 'description', 'diagnosis', 'prescription', 'notes'):
            if field in args:
                setattr(t, field, args[field])
                fields.append(field)
        if fields:
            t.save(update_fields=fields + ['updated_at'])
        return {"id": str(t.id), "updated": True}


@register_tool
class DeletePatientVisit(AssistantTool):
    name = "delete_patient_visit"
    description = "Delete a patient treatment/visit record."
    module_id = "patient_records"
    required_permission = "patient_records.delete_treatment"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"treatment_id": {"type": "string"}},
        "required": ["treatment_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from patient_records.models import Treatment
        try:
            t = Treatment.objects.get(id=args['treatment_id'])
            t.delete()
            return {"deleted": True}
        except Treatment.DoesNotExist:
            return {"error": "Treatment not found"}
