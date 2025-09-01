from rest_framework import serializers
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from ai_summarizer.models import AISummary
from clinical_refs.models import ClinicalReference


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'dob', 'sex', 'national_id', 'primary_doctor_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class EncounterSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    
    class Meta:
        model = Encounter
        fields = ['id', 'patient', 'patient_name', 'occurred_at', 'subjective', 'objective', 
                  'assessment', 'plan', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'patient_name']


class LabResultSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    
    class Meta:
        model = LabResult
        fields = ['id', 'patient', 'patient_name', 'test_name', 'test_code', 'value', 
                  'unit', 'reference_range', 'is_abnormal', 'taken_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'patient_name']


class MedicationOrderSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    
    class Meta:
        model = MedicationOrder
        fields = ['id', 'patient', 'patient_name', 'drug_name', 'drug_code', 'dosage', 
                  'frequency', 'route', 'start_date', 'end_date', 'is_active', 
                  'prescriber_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'patient_name']


class AISummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AISummary
        fields = ['id', 'patient', 'resource_type', 'resource_id', 'summary', 'created_at']
        read_only_fields = ['id', 'created_at']


class ClinicalReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalReference
        fields = ['id', 'title', 'source', 'topic', 'tags', 'content', 'url', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']