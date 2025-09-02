#!/usr/bin/env python3
# demo_script.py - نمایش کامل قابلیت‌های سیستم
import requests
import json
import uuid
import time
import os

BASE_URL = "http://localhost:8000"
TIMEOUT = 10

def main():
    print("🏥 === نمایش سیستم مدیریت بیماران دیابتی ===")
    # نمایش وضعیت امنیتی فقط در محیط توسعه
    if os.getenv('DEBUG', 'True').lower() == 'true':
        print("🔓 سیستم کاملاً باز - بدون نیاز به توکن یا لاگین")
        print("⚠️  فقط برای محیط توسعه - در تولید احراز هویت اضافه کنید")
    
    # 1️⃣ ایجاد بیمار
    print("\n1️⃣ ایجاد بیمار جدید...")
    patient_data = {
        "full_name": "محمد رضایی",
        "sex": "male", 
        "dob": "1975-03-20",
        "national_id": str(uuid.uuid4())[:10],  # استفاده از UUID برای یکتایی
        "primary_doctor_id": str(uuid.uuid4())
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/patients/", json=patient_data, timeout=TIMEOUT)
        if response.status_code != 201:
            print(f"❌ ثبت بیمار شکست خورد: {response.status_code} -> {response.text}")
            return
        patient = response.json()
        patient_id = patient.get('id')
        if not patient_id:
            print("❌ پاسخ سرور شناسه بیمار نداشت")
            return
        print(f"✅ بیمار ایجاد شد: {patient.get('full_name', '—')} (ID: {patient_id})")
    except requests.exceptions.Timeout:
        print("❌ درخواست ایجاد بیمار timeout شد")
        return
    except requests.exceptions.RequestException as e:
        print(f"❌ خطا در ارتباط با سرور: {e}")
        return
    
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
    
    try:
        response = requests.post(f"{BASE_URL}/api/encounters/", json=encounter_data, timeout=TIMEOUT)
        if response.status_code == 201:
            encounter = response.json()
            print(f"✅ ویزیت ثبت شد (ID: {encounter['id']})")
        else:
            print(f"❌ خطا در ثبت ویزیت: {response.status_code} -> {response.text}")
    except requests.exceptions.Timeout:
        print("❌ درخواست ثبت ویزیت timeout شد")
    except requests.exceptions.RequestException as e:
        print(f"❌ خطا در ارتباط با سرور: {e}")
    
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
        
        try:
            response = requests.post(f"{BASE_URL}/api/labs/", json=lab_data, timeout=TIMEOUT)
            if response.status_code == 201:
                print(f"✅ آزمایش {lab['test_name']}: {lab['value']} {lab['unit']}")
            else:
                print(f"❌ خطا در ثبت آزمایش {lab['test_name']}: {response.status_code} -> {response.text}")
        except requests.exceptions.Timeout:
            print(f"❌ درخواست ثبت آزمایش {lab['test_name']} timeout شد")
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در ارتباط با سرور برای آزمایش {lab['test_name']}: {e}")
    
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
        try:
            response = requests.post(f"{BASE_URL}/api/meds/", json=med_data, timeout=TIMEOUT)
            if response.status_code == 201:
                print(f"✅ دارو: {med['drug_name']} {med['dosage']} {med['frequency']}")
            else:
                print(f"❌ خطا در ثبت دارو {med['drug_name']}: {response.status_code} -> {response.text}")
        except requests.exceptions.Timeout:
            print(f"❌ درخواست ثبت دارو {med['drug_name']} timeout شد")
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در ارتباط با سرور برای دارو {med['drug_name']}: {e}")
    
    # 5️⃣ مشاهده Timeline
    print("\n5️⃣ مشاهده Timeline بیمار...")
    # صبر کوتاه تا خلاصه‌سازی/ورژن‌ها ثبت بشن
    time.sleep(2)
    
    try:
        response = requests.get(f"{BASE_URL}/api/patients/{patient_id}/timeline/", timeout=TIMEOUT)
        if response.status_code != 200:
            print(f"❌ خطا در دریافت Timeline: {response.status_code} -> {response.text}")
            return
        timeline = response.json()
    except requests.exceptions.Timeout:
        print("❌ درخواست Timeline timeout شد")
        return
    except requests.exceptions.RequestException as e:
        print(f"❌ خطا در ارتباط با سرور: {e}")
        return
    
    print(f"📊 خلاصه Timeline:")
    print(f"   👤 بیمار: {timeline['patient']['full_name']}")
    print(f"   🏥 تعداد ویزیت‌ها: {len(timeline['encounters'])}")
    print(f"   🧪 تعداد آزمایش‌ها: {len(timeline['labs'])}")
    print(f"   💊 تعداد داروها: {len(timeline['medications'])}")
    print(f"   🧠 تعداد خلاصه‌های AI: {len(timeline['ai_summaries'])}")
    
    # 6️⃣ Export کامل
    print("\n6️⃣ Export کامل اطلاعات...")
    try:
        response = requests.get(f"{BASE_URL}/api/export/patient/{patient_id}/", timeout=TIMEOUT)
        if response.status_code != 200:
            print(f"❌ خطا در Export: {response.status_code} -> {response.text}")
            return
        export_data = response.json()
        
        print(f"📦 Export شامل:")
        print(f"   📋 Metadata: {export_data['export_metadata']}")
        print(f"   🔄 تعداد نسخه‌ها: {len(export_data['versions'])}")
    except requests.exceptions.Timeout:
        print("❌ درخواست Export timeout شد")
    except requests.exceptions.RequestException as e:
        print(f"❌ خطا در ارتباط با سرور: {e}")
    
    # 7️⃣ مشاهده Versioning
    print("\n7️⃣ بررسی نسخه‌گذاری...")
    try:
        response = requests.get(f"{BASE_URL}/api/versions/Patient/{patient_id}/", timeout=TIMEOUT)
        if response.status_code != 200:
            print(f"❌ خطا در دریافت نسخه‌ها: {response.status_code} -> {response.text}")
            return
        versions = response.json()
        print(f"📚 تعداد نسخه‌های Patient: {len(versions)}")
        if versions:
            latest_version = versions[0]
            print(f"   📝 آخرین نسخه: {latest_version['version']} در {latest_version['created_at']}")
    except requests.exceptions.Timeout:
        print("❌ درخواست نسخه‌ها timeout شد")
    except requests.exceptions.RequestException as e:
        print(f"❌ خطا در ارتباط با سرور: {e}")
    
    print(f"\n🎉 تست کامل موفقیت‌آمیز!")
    print(f"🔗 لینک‌های مفید:")
    print(f"   📖 API Docs: {BASE_URL}/api/docs/")
    print(f"   👤 بیمار: {BASE_URL}/api/patients/{patient_id}/")
    print(f"   📋 Timeline: {BASE_URL}/api/patients/{patient_id}/timeline/")
    print(f"   📤 Export: {BASE_URL}/api/export/patient/{patient_id}/")

if __name__ == "__main__":
    main()