from rest_framework import serializers
from patients_core.models import Patient
from diab_encounters.models import Encounter


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'dob', 'sex', 'national_id', 'primary_doctor_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = [
            'id', 'patient', 'occurred_at',
            'subjective', 'objective', 'assessment', 'plan', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

