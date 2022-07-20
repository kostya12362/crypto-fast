from celery import Celery
from settings import config


worker = Celery('sender.tasks', broker=config.get_broker)
worker.autodiscover_tasks(
    [
        'tasks.email',
        'tasks.phone'
    ],
    force=True
)
worker.conf['worker_prefetch_multiplier'] = 1000
