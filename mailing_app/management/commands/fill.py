from django.core.management import BaseCommand

from mailing_app.models import Mailing
from mailing_app.services import start_mailing

CRONJOBS = [
    ('*/5 * * * *', 'mailing_app.cron.other_scheduled_job', ['arg1', 'arg2'], {'verbose': 0}),
    ('0   4 * * *', 'django.core.management.call_command', ['clearsessions']),
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_mailing()
