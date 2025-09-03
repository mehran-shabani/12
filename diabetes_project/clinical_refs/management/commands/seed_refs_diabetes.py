import textwrap
from django.core.management.base import BaseCommand
from clinical_refs.models import ClinicalReference


class Command(BaseCommand):
    help = 'Seed database with diabetes clinical references'

    def handle(self, *args, **options):
        references = [
            {
                "title": "Diabetes Type 2 Management Guidelines",
                "source": "American Diabetes Association",
                "topic": "Diabetes Management",
                "tags": ["diabetes", "type2", "guidelines", "management"],
                "content": """
                Key recommendations for Type 2 Diabetes management:
                1. HbA1c target: <7% for most adults
                2. Blood pressure target: <130/80 mmHg
                3. Lifestyle modifications as first-line therapy
                4. Metformin as first-line medication
                5. Regular monitoring of glucose levels
                6. Annual screening for complications
                """,
                "url": "https://diabetes.org/standards"
            },
            {
                "title": "HbA1c Interpretation Guide",
                "source": "Clinical Laboratory Standards",
                "topic": "Laboratory Tests",
                "tags": ["hba1c", "glycated hemoglobin", "lab", "reference"],
                "content": """
                HbA1c Reference Ranges:
                - Normal: <5.7%
                - Prediabetes: 5.7-6.4%
                - Diabetes: ≥6.5%
                
                Correlation with average glucose:
                - 5%: 97 mg/dL
                - 6%: 126 mg/dL
                - 7%: 154 mg/dL
                - 8%: 183 mg/dL
                - 9%: 212 mg/dL
                - 10%: 240 mg/dL
                """,
                "url": ""
            },
            {
                "title": "Metformin Clinical Use Guide",
                "source": "Pharmacology Reference",
                "topic": "Medications",
                "tags": ["metformin", "medication", "diabetes", "first-line"],
                "content": """
                Metformin (Glucophage):
                - Mechanism: Decreases hepatic glucose production
                - Initial dose: 500mg once or twice daily
                - Maximum dose: 2550mg/day
                - Common side effects: GI upset, diarrhea
                - Contraindications: eGFR <30, acute illness
                - Benefits: Weight neutral, low hypoglycemia risk
                - Monitoring: Renal function, B12 levels
                """,
                "url": ""
            },
            {
                "title": "Diabetic Retinopathy Screening",
                "source": "Ophthalmology Guidelines",
                "topic": "Complications",
                "tags": ["retinopathy", "screening", "complications", "eyes"],
                "content": """
                Screening recommendations:
                - Type 2 DM: At diagnosis and annually
                - Type 1 DM: Within 5 years of diagnosis
                - Pregnancy: Before conception or first trimester
                
                Risk factors:
                - Poor glycemic control
                - Hypertension
                - Duration of diabetes
                - Dyslipidemia
                """,
                "url": ""
            },
            {
                "title": "Insulin Types and Action Profiles",
                "source": "Endocrinology Reference",
                "topic": "Medications",
                "tags": ["insulin", "types", "pharmacology"],
                "content": """
                Insulin Types:
                
                Rapid-acting (Lispro, Aspart):
                - Onset: 15 minutes
                - Peak: 1-2 hours
                - Duration: 4-6 hours
                
                Short-acting (Regular):
                - Onset: 30 minutes
                - Peak: 2-3 hours
                - Duration: 6-8 hours
                
                Long-acting (Glargine, Detemir):
                - Onset: 2 hours
                - No peak
                - Duration: 24 hours
                """,
                "url": ""
            }
        ]
        
        created_count = 0
        updated_count = 0
        for ref_data in references:
            # Remove title from defaults and clean content
            defaults = {k: v for k, v in ref_data.items() if k != "title"}
            if "content" in defaults and isinstance(defaults["content"], str):
                defaults["content"] = textwrap.dedent(defaults["content"]).strip()
            
            ref, created = ClinicalReference.objects.update_or_create(
                title=ref_data["title"],
                defaults=defaults
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {ref.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {ref.title}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully created {created_count} and updated {updated_count} clinical references'
        ))