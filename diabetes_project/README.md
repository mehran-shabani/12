# Diabetes Management System

یک سیستم مدیریت بیماران دیابتی با قابلیت‌های AI و بدون نیاز به احراز هویت.

## ویژگی‌ها

- ✅ مدیریت اطلاعات بیماران
- ✅ ثبت ویزیت‌ها (Encounters)
- ✅ ثبت نتایج آزمایش‌ها
- ✅ مدیریت دارو‌ها
- ✅ خلاصه‌سازی هوشمند با OpenAI
- ✅ Timeline کامل بیمار
- ✅ Export اطلاعات به JSON
- ✅ Versioning تمام تغییرات
- ✅ Clinical References
- ✅ Audit Logging
- ✅ API Documentation (Swagger)

## نصب و راه‌اندازی

### پیش‌نیاز‌ها

- Python 3.11+
- PostgreSQL
- Redis
- MinIO (اختیاری)

### نصب محلی

1. Clone کردن پروژه:
```bash
git clone <repository-url>
cd diabetes_project
```

2. ایجاد محیط مجازی:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. نصب پکیج‌ها:
```bash
pip install -r requirements.txt
```

4. تنظیم متغیرهای محیطی:
```bash
cp .env.example .env
# ویرایش .env و تنظیم مقادیر
```

5. اجرای Migration:
```bash
python manage.py migrate
```

6. ایجاد Superuser (اختیاری):
```bash
python manage.py createsuperuser
```

7. بارگذاری Clinical References:
```bash
python manage.py seed_refs_diabetes
```

8. اجرای سرور:
```bash
python manage.py runserver
```

### اجرا با Docker

```bash
cd infra
docker-compose up -d
```

## استفاده از API

### Health Check
```bash
curl http://localhost:8000/health/
```

### ایجاد بیمار جدید
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "علی احمدی",
    "dob": "1980-01-01",
    "sex": "male",
    "national_id": "1234567890",
    "primary_doctor_id": "00000000-0000-0000-0000-000000000001"
  }'
```

### مشاهده Timeline بیمار
```bash
curl http://localhost:8000/api/patients/{patient_id}/timeline/
```

### API Documentation
http://localhost:8000/api/docs/

## اجرای Celery Workers

برای فعال کردن خلاصه‌سازی AI:

```bash
# Terminal 1 - Worker
celery -A config.celery_app worker -l info

# Terminal 2 - Beat (برای task‌های زمان‌دار)
celery -A config.celery_app beat -l info
```

## تست‌ها

```bash
pytest
# یا برای تست‌های خاص:
pytest tests/test_flow_diabetes.py -v
```

## ساختار پروژه

```
diabetes_project/
├── config/             # تنظیمات Django
├── api/               # ViewSets و Serializers
├── patients_core/     # مدل Patient
├── diab_encounters/   # مدل Encounter
├── diab_labs/        # مدل LabResult
├── diab_medications/ # مدل MedicationOrder
├── ai_summarizer/    # خلاصه‌سازی با AI
├── clinical_refs/    # مراجع بالینی
├── records_versioning/ # سیستم versioning
├── security/         # Audit logging
├── tests/           # تست‌ها
└── infra/           # Docker configuration
```

## نکات امنیتی

⚠️ **توجه**: این پروژه بدون سیستم احراز هویت پیاده‌سازی شده و فقط برای محیط‌های توسعه و تست مناسب است.

برای استفاده در محیط production:
- فعال کردن احراز هویت
- تنظیم CORS محدودتر
- استفاده از HTTPS
- محدود کردن دسترسی به API