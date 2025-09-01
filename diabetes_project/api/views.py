from rest_framework import viewsets
from patients_core.models import Patient
from .serializers import PatientSerializer
from diab_encounters.models import Encounter
from .serializers import EncounterSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = Encounter.objects.all().order_by('-occurred_at')
    serializer_class = EncounterSerializer

from django.shortcuts import render

# Create your views here.
