from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from ai_summarizer.models import AISummary
from .serializers import (
    PatientSerializer, EncounterSerializer, LabResultSerializer,
    MedicationOrderSerializer, AISummarySerializer
)


def export_patient(request, pk):
    """Export all patient data as JSON"""
    try:
        patient = get_object_or_404(Patient, pk=pk)
        
        # Get all related data
        encounters = Encounter.objects.filter(patient=patient).order_by('-occurred_at')
        labs = LabResult.objects.filter(patient=patient).order_by('-taken_at')
        medications = MedicationOrder.objects.filter(patient=patient).order_by('-start_date')
        summaries = AISummary.objects.filter(patient=patient).order_by('-created_at')
        
        # Build export data
        export_data = {
            "export_timestamp": timezone.now().isoformat(),
            "patient": PatientSerializer(patient).data,
            "encounters": EncounterSerializer(encounters, many=True).data,
            "lab_results": LabResultSerializer(labs, many=True).data,
            "medications": MedicationOrderSerializer(medications, many=True).data,
            "ai_summaries": AISummarySerializer(summaries, many=True).data,
            "statistics": {
                "total_encounters": encounters.count(),
                "total_lab_results": labs.count(),
                "total_medications": medications.count(),
                "active_medications": medications.filter(is_active=True).count(),
                "abnormal_labs": labs.filter(is_abnormal=True).count(),
                "total_ai_summaries": summaries.count()
            }
        }
        
        # Create response with appropriate headers
        response = JsonResponse(export_data, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename="patient_{pk}_export.json"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            "error": "Export failed",
            "message": str(e)
        }, status=500)