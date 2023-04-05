from django.apps import AppConfig


class ScheduleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduleapp'

    def ready(self):
        import scheduleapp.scheduler
        scheduleapp.scheduler.start_scheduler()
