from django.contrib.auth import get_user_model  
from celery import shared_task
from django.core.mail import send_mail
from Demo import settings
from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractDay
from datetime import datetime
from Core.models import Students

@shared_task(bind=True)
def send_mail_func(self):
    users = Students.objects.all()
    current_date = datetime.now().date()
    print(current_date)
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        if user.DOB == current_date:
            mail_subject = "Hi! Celery Testing"
            message = f"happy birth day  {user.name} god bless you"
            to_email = user.email
            send_mail(
                subject = mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
        else:
            return "NONE"    
    return "Done"

# from celery import shared_task
# from Core.models import FileUpload
# from Core.serializers import FileSerializer

# @shared_task
# def upload_file_to_db(file_path):
#     with open(file_path, 'rb') as f:
#         file_content = f.read()
#         uploaded_file = FileUpload(file=file_content)
#         uploaded_file.save()


@shared_task
def bday_fun():
    users = Students.objects.all()
    for user in users:
        if user.date_joined and user.date_joined.month == current_date.month and user.date_joined.day == current_date.day:
            message_subject = f'HI {user.username}'
            message = f'Happy birthday {user.username}, God bless you!'
            to_mail = user.email
            send_mail(
                subject=message_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_mail],
                fail_silently=True,
            )
    return "Done"


