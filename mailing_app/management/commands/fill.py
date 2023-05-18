CRONJOBS = [
    ('*/5 * * * *', 'mailing_app.cron.other_scheduled_job', ['arg1', 'arg2'], {'verbose': 0}),
    ('0   4 * * *', 'django.core.management.call_command', ['clearsessions']),
]