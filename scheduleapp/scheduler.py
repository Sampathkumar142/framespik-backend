# import the required modules
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from event.models import OrganizationEventSchedule
from django.utils import timezone
from datetime import date




# define a function to create and schedule multiple jobs
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(task_remainder, 'cron',hour = 6, minute = 30 )
    scheduler.add_job(job2, 'interval', minutes=1)
    scheduler.add_job(job3, 'cron', day_of_week='mon-fri', hour=8, minute=30)
    scheduler.start()

# define the jobs to be scheduled
def task_remainder():
    today = date.today()
    tasks = OrganizationEventSchedule.objects.filter(scheduleAt=today)
    for task in tasks:
        print(task.scheduleAt)
        #code to send the remainder
    

def job2():
    print('Job 2 executed')

def job3():
    print('Job 3 executed')

# call the function to start the scheduler
