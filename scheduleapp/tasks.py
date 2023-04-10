from time import sleep
from celery import shared_task
from googleapiclient.errors import HttpError
from django.core.mail import send_mail,EmailMessage,BadHeaderError,EmailMultiAlternatives
import logging
from event.models import OrganizationEventSchedule
from datetime import date,timedelta
from django.conf import settings
from smtplib import SMTPException
from django.template.loader import render_to_string,get_template
from django.template import Context
from django.utils import timezone
from organization.models import OrganizationSchedule,Organization
from datetime import datetime, timedelta
from django.db.models import Q,F,ExpressionWrapper, FloatField
from accounts.models import Payment,EMIPayment
# from celery import Celery


logger = logging.getLogger(__name__)

#EMAIL Tasks
@shared_task
def sendMail(subject,message,recipients):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_mail =settings.EMAIL_HOST_USER,
            recipient_list= recipients,
            fail_silently=False,
        )
    except BadHeaderError as e:
        logger.info(f"Invalid header found: {e}")
    except SMTPException as e:
        logger.info(f"An error occurred while sending the email: {e}")


@shared_task
def send_email_with_attachments(subject,body,recipients,htmlfile=None,pdfs= [],images=[],context={}):
    try:
        msg = EmailMultiAlternatives(subject, body=body, to=recipients,from_email=settings.EMAIL_HOST_USER)
        if htmlfile:
            html_template = get_template('email_template.html')
            html_content = html_template.render(Context(context))
            msg.attach_alternative(html_content, "text/html")
        for i in pdfs:
            with open(i, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
                msg.attach(i.split('/')[-1], pdf_content, 'application/pdf')
        for j in images:
            with open(j, 'rb') as image_file:
                image_content = image_file.read()
                msg.attach(j.split('/')[-1], image_content, 'image/jpeg')
    except BadHeaderError as e:
        logger.info(f"Invalid header found: {e}")
    except SMTPException as e:
        logger.info(f"An error occurred while sending the email: {e}")
        


@shared_task
def send_mail_template(subject,recipients,template,context =None,):
    try:
        html_content = render_to_string(template, context)
        msg = EmailMessage(subject=subject,body=html_content,from_email=settings.EMAIL_HOST_USER,to=recipients)
        msg.content_subtype = "html"
        msg.send()
    except BadHeaderError as e:
        logger.info(f"Invalid header found: {e}")
    except SMTPException as e:
        logger.info(f"An error occurred while sending the email: {e}")






@shared_task
def eventSchedule():
    today = timezone.now()
    tasks = OrganizationEventSchedule.objects.filter(scheduleAt=today,status = False)
    print(tasks)
    for task in tasks:
        #code for sending through email,mobile,whatsapp
        # code to send the remainder
        pass
    logger.info('Sampath')
    print("sampath")


@shared_task
def organizationSchedule():
    now = timezone.now()
    print(now)
    reminder_time = now + timedelta(minutes=20)
    formatted_time = reminder_time.strftime('%Y-%m-%d %H:%M')
    print(formatted_time)
    my_timezone = timezone.get_default_timezone()
    formatted_now = now.astimezone(my_timezone).strftime('%Y-%m-%d %H:%M')
    print(formatted_now)

    schedules = OrganizationSchedule.objects.filter(
        scheduledAt__exact=formatted_time,
        status=False
    )
    print(schedules)

    for schedule in schedules:
        # Send reminder email here
        # Update status of schedule to avoid sending another reminder
        # schedule.status = True
        # schedule.save()
        p=1





#payment reaminder




# app = Celery('tasks')
# app.conf.beat_schedule = {
#     'send-payment-reminders': {
#         'task': 'myapp.tasks.send_payment_reminders',
#         'schedule': timedelta(hours=1),
#     },
# }

@shared_task
def send_payment_reminders():
    organizations =  Organization.objects.filter(status = 'A')
    today = timezone.now()
    for organization in organizations:
        print(organization.name)
        payment = Payment.objects.filter(
    organization=organization,
    expireDate__gte=today.date()
).first()        
        print('sampath')
        print(payment)
        data = {}
        if payment.emiEnabled ==True:
            bill =  EMIPayment.objects.filter(paymentDate__month = today.month ,status ='Due').first()
            if bill is not None:
                days_until_due = (bill.paymentDate-today.date()).days
                data = {'bill':{
                    'due_date':bill.paymentDate,
                    'amount':bill.amount,
                },
                'organization':{
                    'organization_name':organization.name,
                    'propriter_name':organization.proprietor.name,
                    'proprietor_mobile_number':organization.proprietor.phoneNumber,
                },
                'type':'EMI',
                'days_until_due':days_until_due
                }
        else:
            k = payment.tenure *365.25
            days_until_due = ((payment.date+timedelta(k))-today.date()).days
            data ={'bill':payment,'days_until_due':days_until_due,'type':'DIRECT','organization':organization}

        print(data)
        logger.info(data)
        # days_until_due = (due_date - datetime.now().date()).days

        if days_until_due == 0:
            # Send 6 reminders from 9 am to 9 pm with equal intervals
            
            send_six_reminders(data, timedelta(hours=2))
        
        elif days_until_due in [1,2, 3]:
            # Send 3 reminders at 11 am, 4 pm, and 8 pm every day
            send_three_reminders(data, timedelta(hours=9, minutes=30))
        
        elif days_until_due in [4, 5, 6, 7]:
            # Send 1 reminder every day at 4 pm
            send_one_reminder(data, timedelta(days=1), timedelta(hours=16))
        
        elif days_until_due in range(8, 16):
            # Send 1 reminder every other day at 4 pm
            send_one_reminder(data, timedelta(days=2), timedelta(hours=16))
        
        elif days_until_due in range(16, 32):
            # Send 1 reminder every 3 days at 4 pm
            send_one_reminder(data, timedelta(days=3), timedelta(hours=16))
        
        elif days_until_due in range(32, 61):
            # Send 4 reminders with equal intervals
            send_four_reminders(data, timedelta(days=7))
        
def send_six_reminders(data, interval):
    now = datetime.now()
    start_time = datetime(now.year, now.month, now.day, 9, 0, 0)
    end_time = datetime(now.year, now.month, now.day, 21, 0, 0)
    reminder_time = start_time
    while reminder_time <= end_time:
        send_reminder.apply_async(args=[data],eta= reminder_time)
        reminder_time += interval

def send_three_reminders(data, interval):
    send_reminder.apply_async(args=[data],eta= timezone.now().replace(hour=11, minute=0, second=0))
    send_reminder.apply_async(args=[data], eta=timezone.now().replace(hour=16, minute=0, second=0))
    send_reminder.apply_async(args=[data], eta= timezone.now().replace(hour=20, minute=0, second=0))

def send_one_reminder(data, interval, reminder_time):
    if datetime.now().time() >= reminder_time.time():
        send_reminder.apply_async(args=[data],eta = timezone.now().replace(hour=16, minute=0, second=0) + interval)
    else:
        send_reminder.apply_async(args = [data], eta= timezone.now().replace(hour=16, minute=0, second=0))

def send_four_reminders(data, interval):
    for i in range(4):
        send_reminder.apply_async(args=[data],eta= timezone.now() + (i+1)*interval)



@shared_task
def send_reminder(data):
    print(data)
    pass  # Implement your code to send the reminder here
