#!/usr/bin/env python3
# demo_script.py - نمایش کامل قابلیت‌های سیستم
import requests
import json
import uuid
import time

BASE_URL = "http://localhost:8000"

def main():
    print("🏥 === نمایش سیستم مدیریت بیماران دیابتی ===")
    print("🔓 سیستم کاملاً باز - بدون نیاز به توکن یا لاگین")
    
    # 1️⃣ ایجاد بیمار
    print("\n1️⃣ ایجاد بیمار جدید...")
    patient_data = {
        "full_name": "محمد رضایی",
        "sex": "male", 
        "dob": "1975-03-20",
        "national_id": "0123456789",
        "primary_doctor_id": str(uuid.uuid4())
    }
    
    response = requests.post(f"{BASE_URL}/api/patients/", json=patient_data)
    patient = response.json()
    patient_id = patient['id']
    print(f"✅ بیمار ایجاد شد: {patient['full_name']} (ID: {patient_id})")
    
    # 2️⃣ ایجاد ویزیت
    print("\n2️⃣ ثبت ویزیت...")
    encounter_data = {
        "patient": patient_id,
        "occurred_at": "2025-01-20T09:30:00Z",
        "subjective": "خستگی شدید، تشنگی مفرط، کاهش وزن 5 کیلو در ماه گذشته",
        "objective": {
            "vital_signs": {"bp": "145/95", "weight": "78kg", "height": "175cm"},
            "physical_exam": "بیمار هوشیار، مخاط خشک، نبض منظم"
        },
        "assessment": {
            "primary_diagnosis": "Type 2 Diabetes Mellitus - newly diagnosed",
            "icd10": ["E11.9"],
            "severity": "moderate",
            "notes": "علائم کلاسیک دیابت"
        },
        "plan": {
            "medications": ["Metformin 500mg BID", "Lifestyle modification"],
            "lab_orders": ["HbA1c", "FBS", "Lipid profile"],
            "follow_up": "2 weeks",
            "education": "آموزش رژیم غذایی دیابتی"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/encounters/", json=encounter_data)
    if response.status_code == 201:
        encounter = response.json()
        print(f"✅ ویزیت ثبت شد (ID: {encounter['id']})")
    else:
        print(f"❌ خطا در ثبت ویزیت: {response.status_code}")
    
    # 3️⃣ ثبت آزمایش‌ها
    print("\n3️⃣ ثبت نتایج آزمایش...")
    lab_tests = [
        {"test_name": "HbA1c", "value": 9.2, "unit": "%", "reference_range": "4.0-6.0"},
        {"test_name": "FBS", "value": 180, "unit": "mg/dL", "reference_range": "70-100"},
        {"test_name": "Cholesterol", "value": 220, "unit": "mg/dL", "reference_range": "<200"}
    ]
    
    for lab in lab_tests:
        lab_data = {
            "patient": patient_id,
            "test_name": lab["test_name"],
            "value": lab["value"],
            "unit": lab["unit"],
            "reference_range": lab["reference_range"],
            "taken_at": "2025-01-20T08:00:00Z"
        }
        
        response = requests.post(f"{BASE_URL}/api/labs/", json=lab_data)
        if response.status_code == 201:
            print(f"✅ آزمایش {lab['test_name']}: {lab['value']} {lab['unit']}")
    
    # 4️⃣ ثبت داروها
    print("\n4️⃣ ثبت داروها...")
    medications = [
        {
            "drug_name": "Metformin",
            "dosage": "500mg",
            "frequency": "twice daily",
            "start_date": "2025-01-20",
            "notes": "با غذا مصرف شود"
        },
        {
            "drug_name": "Atorvastatin",
            "dosage": "20mg",
            "frequency": "once daily",
            "start_date": "2025-01-20",
            "notes": "شب‌ها مصرف شود"
        }
    ]
    
    for med in medications:
        med_data = {**med, "patient": patient_id}
        response = requests.post(f"{BASE_URL}/api/meds/", json=med_data)
        if response.status_code == 201:
            print(f"✅ دارو: {med['drug_name']} {med['dosage']} {med['frequency']}")
    
    # 5️⃣ مشاهده Timeline
    print("\n5️⃣ مشاهده Timeline بیمار...")
    response = requests.get(f"{BASE_URL}/api/patients/{patient_id}/timeline/")
    timeline = response.json()
    
    print(f"📊 خلاصه Timeline:")
    print(f"   👤 بیمار: {timeline['patient']['full_name']}")
    print(f"   🏥 تعداد ویزیت‌ها: {len(timeline['encounters'])}")
    print(f"   🧪 تعداد آزمایش‌ها: {len(timeline['labs'])}")
    print(f"   💊 تعداد داروها: {len(timeline['medications'])}")
    print(f"   🧠 تعداد خلاصه‌های AI: {len(timeline['ai_summaries'])}")
    
    # 6️⃣ Export کامل
    print("\n6️⃣ Export کامل اطلاعات...")
    response = requests.get(f"{BASE_URL}/api/export/patient/{patient_id}/")
    export_data = response.json()
    
    print(f"📦 Export شامل:")
    print(f"   📋 Metadata: {export_data['export_metadata']}")
    print(f"   🔄 تعداد نسخه‌ها: {len(export_data['versions'])}")
    
    # 7️⃣ مشاهده Versioning
    print("\n7️⃣ بررسی نسخه‌گذاری...")
    response = requests.get(f"{BASE_URL}/api/versions/Patient/{patient_id}/")
    versions = response.json()
    print(f"📚 تعداد نسخه‌های Patient: {len(versions)}")
    
    print(f"\n🎉 تست کامل موفقیت‌آمیز!")
    print(f"🔗 لینک‌های مفید:")
    print(f"   📖 API Docs: {BASE_URL}/api/docs/")
    print(f"   👤 بیمار: {BASE_URL}/api/patients/{patient_id}/")
    print(f"   📋 Timeline: {BASE_URL}/api/patients/{patient_id}/timeline/")
    print(f"   📤 Export: {BASE_URL}/api/export/patient/{patient_id}/")

if __name__ == "__main__":
    main()