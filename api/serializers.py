# api/serializers.py
from rest_framework import serializers
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'dob', 'sex', 'national_id', 'primary_doctor_id', 'created_at']
        read_only_fields = ['id', 'created_at']

class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = ['id', 'patient', 'occurred_at', 'subjective', 'objective', 'assessment', 'plan', 'created_at']
        read_only_fields = ['id', 'created_at']

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = ['id', 'patient', 'test_name', 'value', 'unit', 'reference_range', 'taken_at', 'created_at']
        read_only_fields = ['id', 'created_at']

class MedicationOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationOrder
        fields = ['id', 'patient', 'drug_name', 'dosage', 'frequency', 'start_date', 'end_date', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']