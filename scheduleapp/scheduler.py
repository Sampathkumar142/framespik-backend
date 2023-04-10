# # import the required modules
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.base import JobLookupError
# from event.models import OrganizationEventSchedule
# from organization.models import OrganizationSchedule
# from django.utils import timezone
# from dateti|me import date,timedelta
# from apscheduler.triggers.cron import CronTrigger



# job_trigger = CronTrigger(hour='9-20', minute='0-59', second='0')


# # define a function to create and schedule multiple jobs
# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(eventSchedule, 'cron',hour = 6, minute = 30 )
#     scheduler.add_job(eventSchedule, 'cron',hour = 10, minute = 0 )
#     scheduler.add_job(organizationSchedule, 'interval', minutes=1)
#     # scheduler.add_job(job2, job_trigger, id='job2')
#     # scheduler.add_job(job2, 'interval', minutes=1)
#     # scheduler.add_job(job3, 'cron', day_of_week='mon-fri', hour=8, minute=30)
#     scheduler.start()

# # define the jobs to be scheduled
# def eventSchedule():
#     today = date.today()
#     tasks = OrganizationEventSchedule.objects.filter(scheduleAt=today)
#     for task in tasks:
#         print(task.scheduleAt)
#         #code to send the remainder
    

# def organizationSchedule():
#     now = timezone.now()
#     print(now)
#     reminder_time = now + timedelta(minutes=20)
#     formatted_time = reminder_time.strftime('%Y-%m-%d %H:%M')
#     print(formatted_time)
#     my_timezone = timezone.get_default_timezone()
#     formatted_now = now.astimezone(my_timezone).strftime('%Y-%m-%d %H:%M')
#     print(formatted_now)

#     schedules = OrganizationSchedule.objects.filter(
#         scheduledAt__exact=formatted_time,
#         status=False
#     )
#     print(schedules)

#     for schedule in schedules:
#         # Send reminder email here
#         # Update status of schedule to avoid sending another reminder
#         # schedule.status = True
#         # schedule.save()
#         p=1


# #from 9 to evening  9 hour ki 6 hours ki okkasari  job jaragali 
# #last 3 days vunte day ki 3 times 11,4,8
# def paymentremainder(): #phonenumber 
#     print('Job 3 executed')
# #last 1 week vunte day ki 1 time  4
# #last 8 to 15 days vunte alternative days lo 1 time at 6
# #16 to 31 days vunte 3days ki once message vellali
# # account is inactive message couldn't be send 

# # call the function to start the scheduler

# #last month lo 4 times vellali 1,10,20,30
# def paymentWhatsappremainder():
#     pass

# #event wish every day once on behalf of photographer
# def eventwish():
#     pass

# #messages should sent every 15mins 
# def bulkinvitation():
#     pass

# #if anyone payment is paid after due of one month payment will get inactive  at 12AM
# def checkAccountStatus():
#     pass
