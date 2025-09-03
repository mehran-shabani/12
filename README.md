# 🏥 Diabetes Pilot API - سیستم مدیریت بیماران دیابتی

یک سیستم کامل مدیریت بیماران دیابتی با قابلیت‌های هوش مصنوعی، نسخه‌گذاری و تحلیل داده‌های بالینی.

## ✨ ویژگی‌های کلیدی

- 🔓 **API کاملاً باز** - بدون نیاز به احراز هویت یا توکن
- 🧠 **خلاصه‌سازی با AI** - تولید خودکار خلاصه برای تمام رکوردهای بالینی
- 📋 **Timeline کامل** - نمای زمانی کامل فعالیت‌های بیمار
- 🔄 **Versioning** - نسخه‌گذاری تمام تغییرات داده‌ها
- 📤 **Export** - خروجی کامل اطلاعات بیمار
- 🔍 **OpenAPI Docs** - مستندات کامل API

## 🏗 ساختار پروژه

```
diabetes_project/
├── config/                 # تنظیمات Django
├── api/                    # API endpoints و serializers
├── patients_core/          # مدل بیمار
├── diab_encounters/        # مدل ویزیت‌ها
├── diab_labs/             # مدل آزمایش‌ها
├── diab_medications/      # مدل داروها
├── ai_summarizer/         # خلاصه‌سازی با OpenAI
├── records_versioning/    # سیستم نسخه‌گذاری
└── tests/                 # تست‌های کامل
```

## 🚀 راه‌اندازی

### 1. نصب dependencies
```bash
pip install -r requirements.txt
```

### 2. تنظیم environment variables
```bash
cp .env.example .env
# ویرایش .env و اضافه کردن OPENAI_API_KEY
```

### 3. اجرای migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. راه‌اندازی سرور
```bash
python manage.py runserver
```

## 📡 API Endpoints

### 🧑‍⚕️ بیماران
- `GET /api/patients/` - لیست بیماران
- `POST /api/patients/` - ایجاد بیمار جدید
- `GET /api/patients/{id}/` - جزئیات بیمار
- `PUT/PATCH /api/patients/{id}/` - ویرایش بیمار
- `DELETE /api/patients/{id}/` - حذف بیمار
- `GET /api/patients/{id}/timeline/` - تایم‌لاین کامل بیمار

### 🏥 ویزیت‌ها
- `GET /api/encounters/` - لیست ویزیت‌ها
- `POST /api/encounters/` - ثبت ویزیت جدید
- `GET /api/encounters/{id}/` - جزئیات ویزیت

### 🧪 آزمایش‌ها
- `GET /api/labs/` - لیست آزمایش‌ها
- `POST /api/labs/` - ثبت آزمایش جدید
- `GET /api/labs/{id}/` - جزئیات آزمایش

### 💊 داروها
- `GET /api/meds/` - لیست داروها
- `POST /api/meds/` - ثبت دارو جدید
- `GET /api/meds/{id}/` - جزئیات دارو

### 📤 Export و Versioning
- `GET /api/export/patient/{id}/` - export کامل اطلاعات بیمار
- `GET /api/versions/{resource_type}/{resource_id}/` - تاریخچه نسخه‌ها
- `POST /api/versions/revert/` - بازگردانی به نسخه قبل

## 🧪 تست‌ها

```bash
# اجرای تمام تست‌ها
pytest tests/ -v

# تست‌های مشخص
pytest tests/test_basic_flow.py -v
pytest tests/test_complete_flow.py -v
pytest tests/test_versioning.py -v
pytest tests/test_export.py -v
```

## 📖 مستندات API

مستندات کامل API در آدرس زیر قابل دسترسی است:
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## 🔧 Celery (اختیاری)

برای فعال‌سازی خلاصه‌سازی خودکار با AI:

```bash
# راه‌اندازی Redis
docker run -d -p 6379:6379 redis:alpine

# راه‌اندازی Celery Worker
celery -A config.celery_app worker -l info
```

## 🧬 نمونه استفاده

### ایجاد بیمار
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "علی احمدی",
    "sex": "male",
    "dob": "1980-05-15",
    "primary_doctor_id": "00000000-0000-0000-0000-000000000111"
  }'
```

### ثبت ویزیت
```bash
curl -X POST http://localhost:8000/api/encounters/ \
  -H "Content-Type: application/json" \
  -d '{
    "patient": "PATIENT_ID",
    "occurred_at": "2025-01-15T10:00:00Z",
    "subjective": "خستگی و تشنگی مفرط",
    "objective": {"bp": "140/90", "weight": "80kg"},
    "assessment": {"icd10": ["E11"]},
    "plan": {"medication": "Metformin"}
  }'
```

### مشاهده Timeline
```bash
curl http://localhost:8000/api/patients/PATIENT_ID/timeline/
```

## 🛡 امنیت

⚠️ **توجه**: این پروژه برای محیط توسعه طراحی شده و تمام APIها بدون احراز هویت قابل دسترسی هستند. برای استفاده در محیط تولید، سیستم احراز هویت مناسب اضافه کنید.

## 📝 License

این پروژه تحت مجوز MIT منتشر شده است.