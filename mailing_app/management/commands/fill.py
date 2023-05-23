from django.core.management import BaseCommand

from mailing_app.services import client_mailing

CRONJOBS = [
    ('*/5 * * * *', 'mailing_app.cron.other_scheduled_job', ['arg1', 'arg2'], {'verbose': 0}),
    ('0   4 * * *', 'django.core.management.call_command', ['clearsessions']),
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        client_mailing()
