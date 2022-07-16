from __future__ import absolute_import

import datetime
import os

from . import settings

from celery import Celery
from celery.schedules import crontab

# ../env/Scripts/celery -A Accounting.celeryfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Accounting.settings')

app = Celery('Accounting', broker=settings.cache_backend, backend=settings.cache_backend)

app.conf.result_expires = datetime.timedelta(seconds=15)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.uses_utc_timezone()

app.conf.beat_schedule = {
    'bill_task_Daily': {
        'task': 'app_Utils.tasks.bill_task',
        'schedule': crontab(minute=0, hour=0)
    },
}
app.autodiscover_tasks()
