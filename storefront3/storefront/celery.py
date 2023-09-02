# File for configuring celery
import os
from celery import Celery

# Set environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev')

# Create celery object
celery = Celery('storefront')
# Load celery config from settings.py
celery.config_from_object('django.conf:settings', namespace='CELERY')
# Set celery to auto discover tasks in tasks.py
celery.autodiscover_tasks()
