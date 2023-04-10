from django.apps import AppConfig


class ScheduleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduleapp'

    # def ready(self):
    #     from django_celery_beat.schedulers import DatabaseScheduler
    #     from django.conf import settings
    #     DatabaseScheduler.update_from_dict(settings.CELERY_BEAT_SCHEDULE)
        # from .models import PeriodicTask

        # # Update the database with the schedule
        # PeriodicTask.objects.update_from_dict(settings.CELERY_BEAT_SCHEDULE)
