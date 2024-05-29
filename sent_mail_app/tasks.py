from django.contrib.auth import get_user_model  
from celery import shared_task
from django.core.mail import send_mail
from Demo import settings
from django.utils import timezone

@shared_task(bind=True)
def send_mail_func(self):
    user=get_user_model().objects.all()
    for users in user:
        message_subject="Hi ! Celery Testing"
        message="I test my django application and use to celery send a mail to user "
        to_mail=users.email
        send_mail(
            subject=message_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_mail],
            fail_silently=True,
        )
    return "Done"





