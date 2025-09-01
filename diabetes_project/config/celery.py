import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create celery app
celery_app = Celery('config')

# Load config from Django settings
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
celery_app.autodiscover_tasks()