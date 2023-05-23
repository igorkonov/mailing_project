from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing_app.models import Mailing, MailingAttempt


def client_mailing():
    mailing_items = Mailing.objects.filter(mailing_status='created', mailing_time__lte=timezone.now())
    for item in mailing_items:
        clients = item.clients.all()
        for client in clients:
            mailing_attempt = MailingAttempt.objects.create(mailing=item, client=client, status='pending')
            send_mail(
                subject=item.message.subject,
                message=item.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )
            mailing_attempt.status = 'sent'
            mailing_attempt.save()
        item.mailing_status = 'finished'
        item.save()
