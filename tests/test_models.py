"""Tests for patient_records models."""
import pytest
from django.utils import timezone

from patient_records.models import PatientRecord, Treatment


@pytest.mark.django_db
class TestPatientRecord:
    """PatientRecord model tests."""

    def test_create(self, patient_record):
        """Test PatientRecord creation."""
        assert patient_record.pk is not None
        assert patient_record.is_deleted is False

    def test_soft_delete(self, patient_record):
        """Test soft delete."""
        pk = patient_record.pk
        patient_record.is_deleted = True
        patient_record.deleted_at = timezone.now()
        patient_record.save()
        assert not PatientRecord.objects.filter(pk=pk).exists()
        assert PatientRecord.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, patient_record):
        """Test default queryset excludes deleted."""
        patient_record.is_deleted = True
        patient_record.deleted_at = timezone.now()
        patient_record.save()
        assert PatientRecord.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, patient_record):
        """Test toggling is_active."""
        original = patient_record.is_active
        patient_record.is_active = not original
        patient_record.save()
        patient_record.refresh_from_db()
        assert patient_record.is_active != original


@pytest.mark.django_db
class TestTreatment:
    """Treatment model tests."""

    def test_create(self, treatment):
        """Test Treatment creation."""
        assert treatment.pk is not None
        assert treatment.is_deleted is False

    def test_soft_delete(self, treatment):
        """Test soft delete."""
        pk = treatment.pk
        treatment.is_deleted = True
        treatment.deleted_at = timezone.now()
        treatment.save()
        assert not Treatment.objects.filter(pk=pk).exists()
        assert Treatment.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, treatment):
        """Test default queryset excludes deleted."""
        treatment.is_deleted = True
        treatment.deleted_at = timezone.now()
        treatment.save()
        assert Treatment.objects.filter(hub_id=hub_id).count() == 0


