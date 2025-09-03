# records_versioning/apps.py
from django.apps import AppConfig

class RecordsVersioningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'records_versioning'

    def ready(self):
        import records_versioning.signals  # noqa