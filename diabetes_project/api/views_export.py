from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.conf import settings
import logging
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from ai_summarizer.models import AISummary
from .serializers import (
    PatientSerializer, EncounterSerializer, LabResultSerializer,
    MedicationOrderSerializer, AISummarySerializer
)

logger = logging.getLogger(__name__)


@require_GET
def export_patient(request, pk):
    """Export all patient data as JSON"""
    # Let Http404 bubble up if the patient doesn't exist
    patient = get_object_or_404(Patient, pk=pk)
    
    # Security check - temporary guard until proper DRF permissions
    # TODO: Replace with proper DRF ViewSet action with IsAdminUser permission
    expected_token = getattr(settings, "ADMIN_EXPORT_TOKEN", None)
    if expected_token and request.headers.get("X-Export-Token") != expected_token:
        logger.warning("Failed export attempt for patient %s from IP %s", pk, request.META.get('REMOTE_ADDR'))
        return JsonResponse({"error": "Forbidden"}, status=403)
    
    try:
        # Get all related data with optimized queries
        encounters_qs = Encounter.objects.filter(patient=patient).select_related('patient').order_by('-occurred_at')
        labs_qs = LabResult.objects.filter(patient=patient).select_related('patient').order_by('-taken_at')
        medications_qs = MedicationOrder.objects.filter(patient=patient).select_related('patient').order_by('-start_date')
        summaries_qs = AISummary.objects.filter(patient=patient).order_by('-created_at')
        
        # Materialize querysets to avoid multiple DB hits
        encounters = list(encounters_qs)
        labs = list(labs_qs)
        medications = list(medications_qs)
        summaries = list(summaries_qs)
        
        # Build export data
        export_data = {
            "export_timestamp": timezone.now().isoformat(),
            "patient": PatientSerializer(patient).data,
            "encounters": EncounterSerializer(encounters, many=True).data,
            "lab_results": LabResultSerializer(labs, many=True).data,
            "medications": MedicationOrderSerializer(medications, many=True).data,
            "ai_summaries": AISummarySerializer(summaries, many=True).data,
            "statistics": {
                "total_encounters": len(encounters),
                "total_lab_results": len(labs),
                "total_medications": len(medications),
                "active_medications": sum(1 for m in medications if m.is_active),
                "abnormal_labs": sum(1 for l in labs if l.is_abnormal),
                "total_ai_summaries": len(summaries)
            }
        }
        
        # Create response with appropriate headers
        response = JsonResponse(export_data, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename="patient_{pk}_export.json"'
        
        return response
        
    except Exception:
        logger.exception("Export failed for patient %s", pk)
        return JsonResponse({"error": "Export failed"}, status=500)