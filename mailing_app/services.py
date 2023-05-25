from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing_app.models import Mailing, MailingAttempt, Client


def send_message(mailing):
    status_list = []
    client = mailing.clients.all()
    for item in client:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[item.email],
                fail_silently=False
            )
        except:
            server_response = {'time': timezone.now().astimezone(settings.TIME_ZONE),
                               'status': MailingAttempt.FAILED,
                               'server_response': item.email,
                               'mailing': Mailing.objects.get(pk=mailing.id),
                               'clients': Client.objects.get(pk=mailing.client.id)}
            status_list.append(MailingAttempt(**server_response))
        else:
            server_response = {'time': timezone.now().astimezone(settings.TIME_ZONE),
                               'status': MailingAttempt.SENT,
                               'server_response': item.email,
                               'mailing': Mailing.objects.get(pk=mailing.id),
                               'clients': Client.objects.get(pk=mailing.client.id)}
            status_list.append(MailingAttempt(**server_response))
    MailingAttempt.objects.bulk_create(status_list)


def start_mailing():
    mailings = Mailing.objects.all()
    for mailing in mailings:
        if mailing.mailing_status == Mailing.STARTED:
            obj = MailingAttempt.objects.filter(mailing_pk=mailing.id).last()

            if obj is None:
                mailing_time = mailing.mailing_time.replace(second=0)
                time_now = timezone.now().time().replace(second=0)

                if mailing_time == time_now:
                    send_message(mailing)

            else:
                frequency = mailing.frequency
                obj_time = obj.time

                if frequency == Mailing.DAILY:
                    obj_time += timezone.timedelta(days=1)
                elif frequency == Mailing.WEEKLY:
                    obj_time += timezone.timedelta(days=7)
                elif frequency == Mailing.MONTHLY:
                    obj_time += timezone.timedelta(days=30)

                obj_time = obj_time.replace(second=0)
                time_now = timezone.now().replace(second=0)

                if obj_time == time_now:
                    send_message(mailing)
