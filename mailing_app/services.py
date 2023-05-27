from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from mailing_app.models import Mailing, MailingAttempt
import datetime


def start_mailing():
    # Получить все рассылки со статусом СОЗДАН
    mailings = Mailing.objects.filter(mailing_status=Mailing.CREATED)
    print(mailings)
    for mailing in mailings:
        # Рассчитать дату последнего запуска на основе периодичности
        last_run_date = None

        if mailing.frequency == Mailing.DAILY:
            yesterday = timezone.now() - datetime.timedelta(days=1)
            last_run_date = datetime.datetime.combine(yesterday.date(), mailing.mailing_time)

        elif mailing.frequency == Mailing.WEEKLY:
            last_week = timezone.now() - datetime.timedelta(weeks=1)
            last_run_date = datetime.datetime.combine(last_week.date(), mailing.mailing_time)

        elif mailing.frequency == Mailing.MONTHLY:
            last_month = timezone.now() - datetime.timedelta(days=30)
            last_run_date = datetime.datetime.combine(last_month.date(), mailing.mailing_time)

        # Проверяем, не предшествует ли дата последнего запуска сегодняшнему дню
        if last_run_date.date() < timezone.now().date():
            # Получить всех клиентов в рассылке
            clients = mailing.clients.all()

            # Отправить сообщение каждому клиенту
            for client in clients:
                try:
                    send_mail(subject=mailing.message.subject,
                              message=mailing.message.body,
                              from_email=settings.EMAIL_HOST_USER,
                              recipient_list=[client.email],
                              fail_silently=False)

                    status = MailingAttempt.SENT
                    server_response = 'Сообщение успешно отправлено'
                except Exception as e:
                    status = MailingAttempt.FAILED
                    server_response = 'Ошибка при отправке сообщения: {}'.format(str(e))

                MailingAttempt.objects.create(
                    status=status,
                    server_response=server_response,
                    mailing=mailing
                )

            # Обновление статуса рассылки
            if mailing.mailing_status == Mailing.CREATED:
                mailing.mailing_status = Mailing.STARTED
            else:
                mailing.mailing_status = Mailing.FINISHED
            mailing.save()
