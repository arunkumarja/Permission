#environment Setup
from __future__ import absolute_import,unicode_literals
import os 
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

#Django Settings Module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Demo.settings')


#creating celery app
app=Celery('Demo')
app.conf.enable_utc=False

#config the celery app
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')

#celery beat settings
app.conf.beat_schedule={
    # 'send-mail-everyday-at-9':{
    #    'task' :'sent_mail_app.tasks.send_mail_func',
    #    'schedule':crontab(hour=10,minute=3)
    # }

    
}
#auto discover task
app.autodiscover_tasks()

#debug task
@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
