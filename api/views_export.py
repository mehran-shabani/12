# api/views_export.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from ai_summarizer.models import AISummary
from records_versioning.models import RecordVersion
from django.core.serializers.json import DjangoJSONEncoder
import json

def export_patient(request, pk):
    """Export کامل اطلاعات بیمار به فرمت JSON"""
    
    try:
        patient = Patient.objects.get(pk=pk)
        
        # جمع‌آوری تمام داده‌های مرتبط
        encounters = Encounter.objects.filter(patient=patient).order_by('-occurred_at')
        labs = LabResult.objects.filter(patient=patient).order_by('-taken_at')
        medications = MedicationOrder.objects.filter(patient=patient).order_by('-start_date')
        ai_summaries = AISummary.objects.filter(patient=patient).order_by('-created_at')
        versions = RecordVersion.objects.filter(
            resource_type='Patient',
            resource_id=patient.id
        ).order_by('-version')
        
        # تبدیل به dictionary
        export_data = {
            "patient": {
                "id": str(patient.id),
                "full_name": patient.full_name,
                "dob": patient.dob.isoformat() if patient.dob else None,
                "sex": patient.sex,
                "national_id": patient.national_id,
                "primary_doctor_id": str(patient.primary_doctor_id),
                "created_at": patient.created_at.isoformat()
            },
            "encounters": [
                {
                    "id": str(e.id),
                    "occurred_at": e.occurred_at.isoformat(),
                    "subjective": e.subjective,
                    "objective": e.objective,
                    "assessment": e.assessment,
                    "plan": e.plan,
                    "created_at": e.created_at.isoformat()
                } for e in encounters
            ],
            "lab_results": [
                {
                    "id": str(l.id),
                    "test_name": l.test_name,
                    "value": l.value,
                    "unit": l.unit,
                    "reference_range": l.reference_range,
                    "taken_at": l.taken_at.isoformat(),
                    "created_at": l.created_at.isoformat()
                } for l in labs
            ],
            "medications": [
                {
                    "id": str(m.id),
                    "drug_name": m.drug_name,
                    "dosage": m.dosage,
                    "frequency": m.frequency,
                    "start_date": m.start_date.isoformat() if hasattr(m.start_date, 'isoformat') else str(m.start_date),
                    "end_date": m.end_date.isoformat() if m.end_date and hasattr(m.end_date, 'isoformat') else str(m.end_date) if m.end_date else None,
                    "notes": m.notes,
                    "created_at": m.created_at.isoformat()
                } for m in medications
            ],
            "ai_summaries": [
                {
                    "id": str(s.id),
                    "resource_type": s.resource_type,
                    "resource_id": str(s.resource_id),
                    "summary": s.summary,
                    "created_at": s.created_at.isoformat()
                } for s in ai_summaries
            ],
            "versions": [
                {
                    "version": v.version,
                    "snapshot": v.snapshot,
                    "diff": v.diff,
                    "created_at": v.created_at.isoformat()
                } for v in versions
            ],
            "export_metadata": {
                "export_date": json.dumps(patient.created_at, cls=DjangoJSONEncoder),
                "total_encounters": encounters.count(),
                "total_labs": labs.count(),
                "total_medications": medications.count(),
                "total_summaries": ai_summaries.count()
            }
        }
        
        return JsonResponse(export_data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
        
    except Patient.DoesNotExist:
        return JsonResponse({
            "error": "بیمار یافت نشد"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "error": "خطا در export اطلاعات بیمار",
            "details": str(e)
        }, status=500)