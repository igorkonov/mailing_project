from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta

from django.utils import timezone

from mailing_app.models import Mailing, MailingAttempt, Client
import pytz
import datetime


def send_message(subject, message, from_email, recipient_list, fail_silently):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently,
    )
#         status = MailingAttempt.SENT
#
#     except Exception as e:
#         status = MailingAttempt.FAILED
#         print(e)
#     server_response = {
#         'time': datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE)),
#         'status': status,
#         'server_response': client.email,
#         'mailing': mailing,
#         'client': client,
#     }
#     MailingAttempt.objects.create(**server_response)


def start_mailing():
    # Get all mailings with the CREATED status
    mailings = Mailing.objects.filter(mailing_status=Mailing.CREATED)

    for mailing in mailings:
        # Calculate the last run date based on the frequency
        last_run_date = None

        if mailing.frequency == Mailing.DAILY:
            last_run_date = mailing.created.date()
        elif mailing.frequency == Mailing.WEEKLY:
            last_run_date = mailing.created.date() - datetime.timedelta(weeks=1)
        elif mailing.frequency == Mailing.MONTHLY:
            last_run_date = mailing.created.date() - datetime.timedelta(days=30)

        # Check if the last run date is before today
        if last_run_date and last_run_date < timezone.now().date():
            # Get all clients in the mailing
            clients = mailing.clients.all()

            # Send the message to each client
            for client in clients:
                try:

                    subject = mailing.message.subject
                    message = mailing.message.body
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [client.email]
                    fail_silently = False,
                    send_mail(subject, message, from_email, recipient_list, fail_silently)
                    status = MailingAttempt.SENT
                    server_response = None
                except Exception as e:
                    status = MailingAttempt.FAILED
                    server_response = str(e)

                MailingAttempt.objects.create(
                    status=status,
                    server_response=server_response,
                    mailing=mailing
                )
            # Update the mailing status
            if mailing.mailing_status == Mailing.CREATED:
                mailing.mailing_status = Mailing.STARTED
            else:
                mailing.mailing_status = Mailing.FINISHED
            mailing.save()
