import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab
from celery.signals import worker_ready

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coin_mena_challenge.settings")
app = Celery("coin_mena_challenge")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-retrieve-rates-from-alpha-vantage-every-1-hour': {
        'task': 'quotes.tasks.retrieve_rates_from_alpha_vantage',
        'schedule': crontab(minute=0)
    }
}


@worker_ready.connect
def at_start(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task("quotes.tasks.retrieve_rates_from_alpha_vantage", connection=conn)
