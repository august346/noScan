from celery import Celery
from celery.schedules import crontab

import db

db.meta.create_all()
app = Celery(broker='amqp://guest:guest@localhost:5672/', backend='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'collect-every-night': {
        'task': 'celery_tasks.collect_full',
        'schedule': crontab(minute=0, hour=0),
    },
    'collect-likes-every-6-hour': {
        'task': 'celery_tasks.collect_likes',
        'schedule': crontab(minute=0, hour='*/3'),
    },
}
