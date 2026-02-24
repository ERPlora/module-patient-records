"""Tests for patient_records views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('patient_records:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('patient_records:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('patient_records:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestPatientRecordViews:
    """PatientRecord view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('patient_records:patient_records_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('patient_records:patient_records_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('patient_records:patient_records_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('patient_records:patient_records_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('patient_records:patient_records_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('patient_records:patient_records_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('patient_records:patient_record_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('patient_records:patient_record_add')
        data = {
            'patient_name': 'New Patient Name',
            'date_of_birth': '2025-01-15',
            'gender': 'New Gender',
            'blood_type': 'New Blood Type',
            'allergies': 'Test description',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, patient_record):
        """Test edit form loads."""
        url = reverse('patient_records:patient_record_edit', args=[patient_record.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, patient_record):
        """Test editing via POST."""
        url = reverse('patient_records:patient_record_edit', args=[patient_record.pk])
        data = {
            'patient_name': 'Updated Patient Name',
            'date_of_birth': '2025-01-15',
            'gender': 'Updated Gender',
            'blood_type': 'Updated Blood Type',
            'allergies': 'Test description',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, patient_record):
        """Test soft delete via POST."""
        url = reverse('patient_records:patient_record_delete', args=[patient_record.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        patient_record.refresh_from_db()
        assert patient_record.is_deleted is True

    def test_toggle_status(self, auth_client, patient_record):
        """Test toggle active status."""
        url = reverse('patient_records:patient_record_toggle_status', args=[patient_record.pk])
        original = patient_record.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        patient_record.refresh_from_db()
        assert patient_record.is_active != original

    def test_bulk_delete(self, auth_client, patient_record):
        """Test bulk delete."""
        url = reverse('patient_records:patient_records_bulk_action')
        response = auth_client.post(url, {'ids': str(patient_record.pk), 'action': 'delete'})
        assert response.status_code == 200
        patient_record.refresh_from_db()
        assert patient_record.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('patient_records:patient_records_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestTreatmentViews:
    """Treatment view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('patient_records:treatments_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('patient_records:treatments_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('patient_records:treatments_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('patient_records:treatments_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('patient_records:treatments_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('patient_records:treatments_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('patient_records:treatment_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('patient_records:treatment_add')
        data = {
            'date': '2025-01-15',
            'description': 'Test description',
            'diagnosis': 'Test description',
            'prescription': 'Test description',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, treatment):
        """Test edit form loads."""
        url = reverse('patient_records:treatment_edit', args=[treatment.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, treatment):
        """Test editing via POST."""
        url = reverse('patient_records:treatment_edit', args=[treatment.pk])
        data = {
            'date': '2025-01-15',
            'description': 'Test description',
            'diagnosis': 'Test description',
            'prescription': 'Test description',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, treatment):
        """Test soft delete via POST."""
        url = reverse('patient_records:treatment_delete', args=[treatment.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        treatment.refresh_from_db()
        assert treatment.is_deleted is True

    def test_bulk_delete(self, auth_client, treatment):
        """Test bulk delete."""
        url = reverse('patient_records:treatments_bulk_action')
        response = auth_client.post(url, {'ids': str(treatment.pk), 'action': 'delete'})
        assert response.status_code == 200
        treatment.refresh_from_db()
        assert treatment.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('patient_records:treatments_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('patient_records:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('patient_records:settings')
        response = client.get(url)
        assert response.status_code == 302

