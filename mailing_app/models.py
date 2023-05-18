from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='контактный email')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comments = models.CharField(max_length=500, **NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    mailing_time = models.TimeField(verbose_name='Время рассылки')
    frequency = models.CharField(verbose_name='Периодичность')
    mailing_status = models.CharField(verbose_name='Статус рассылки')

    def __str__(self):
        return self.mailing_time

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class MailingAttempt(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(verbose_name='статус попытки')
    server_response = models.CharField(**NULLABLE, verbose_name='ответ почтового сервера')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f'{str(self.time)} - {self.status}'
