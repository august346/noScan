from celery import Celery
from celery.schedules import crontab

app = Celery()


app.conf.beat_schedule = {
    'add-every-night': {
        'task': 'tasks.collect_empties',
        'schedule': crontab(minute=0, hour=0),
    },
}
