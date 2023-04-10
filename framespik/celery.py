import os 
from celery import Celery
import pytz

# PeriodicTask.objects.update_from_dict(settings.CELERY_BEAT_SCHEDULE)
# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'framespik.settings')

# Create a Celery instance
celery = Celery('framespik')

# Load Celery settings from Django settings
celery.config_from_object('django.conf:settings', namespace='CELERY')
# celery.conf.broker_url = 'redis://localhost:6379'
# Discover tasks in all installed Django apps
celery.conf.timezone = 'Asia/Kolkata'


celery.autodiscover_tasks()

# Define the default queue for tasks
