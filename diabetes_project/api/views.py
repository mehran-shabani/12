from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from ai_summarizer.models import AISummary
from clinical_refs.models import ClinicalReference
from .serializers import (
    PatientSerializer, EncounterSerializer, LabResultSerializer,
    MedicationOrderSerializer, AISummarySerializer, ClinicalReferenceSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get complete timeline of patient's medical records"""
        patient = self.get_object()
        
        # Get all related records
        encounters = Encounter.objects.filter(patient=patient).order_by('-occurred_at')[:10]
        labs = LabResult.objects.filter(patient=patient).order_by('-taken_at')[:20]
        meds = MedicationOrder.objects.filter(patient=patient).order_by('-start_date')[:20]
        summaries = AISummary.objects.filter(patient=patient).order_by('-created_at')[:10]
        
        return Response({
            "patient": PatientSerializer(patient).data,
            "encounters": EncounterSerializer(encounters, many=True).data,
            "labs": LabResultSerializer(labs, many=True).data,
            "medications": MedicationOrderSerializer(meds, many=True).data,
            "ai_summaries": AISummarySerializer(summaries, many=True).data,
            "stats": {
                "total_encounters": encounters.count(),
                "total_labs": labs.count(),
                "active_medications": meds.filter(is_active=True).count(),
                "total_summaries": summaries.count()
            }
        })

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get patient summary statistics"""
        patient = self.get_object()
        
        stats = {
            "encounters_count": patient.encounters.count(),
            "lab_results_count": patient.lab_results.count(),
            "medications_count": patient.medications.count(),
            "active_medications": patient.medications.filter(is_active=True).count(),
            "ai_summaries_count": patient.ai_summaries.count(),
            "recent_encounter": None,
            "abnormal_labs_count": patient.lab_results.filter(is_abnormal=True).count()
        }
        
        # Get most recent encounter
        recent_encounter = patient.encounters.order_by('-occurred_at').first()
        if recent_encounter:
            stats["recent_encounter"] = {
                "id": str(recent_encounter.id),
                "occurred_at": recent_encounter.occurred_at,
                "subjective": recent_encounter.subjective[:100] + "..." if len(recent_encounter.subjective) > 100 else recent_encounter.subjective
            }
        
        return Response(stats)


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = Encounter.objects.all().order_by('-occurred_at')
    serializer_class = EncounterSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset


class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all().order_by('-taken_at')
    serializer_class = LabResultSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by abnormal results
        abnormal = self.request.query_params.get('abnormal', None)
        if abnormal and abnormal.lower() == 'true':
            queryset = queryset.filter(is_abnormal=True)
        
        # Filter by test name
        test_name = self.request.query_params.get('test_name', None)
        if test_name:
            queryset = queryset.filter(test_name__icontains=test_name)
        
        return queryset


class MedicationOrderViewSet(viewsets.ModelViewSet):
    queryset = MedicationOrder.objects.all().order_by('-start_date')
    serializer_class = MedicationOrderSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by active medications
        active = self.request.query_params.get('active', None)
        if active and active.lower() == 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset


class ClinicalReferenceViewSet(viewsets.ModelViewSet):
    queryset = ClinicalReference.objects.all().order_by('topic', 'title')
    serializer_class = ClinicalReferenceSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by topic
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(topic__icontains=topic)
        
        # Search in title and content
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(tags__contains=search)
            )
        
        return queryset