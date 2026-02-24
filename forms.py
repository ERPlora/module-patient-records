from django import forms
from django.utils.translation import gettext_lazy as _

from .models import PatientRecord, Treatment

class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['patient_name', 'date_of_birth', 'gender', 'blood_type', 'allergies', 'medical_notes', 'is_active']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'gender': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'blood_type': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'allergies': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'medical_notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['patient', 'date', 'description', 'diagnosis', 'prescription', 'practitioner_id', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'prescription': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'practitioner_id': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

