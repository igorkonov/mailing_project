from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='контактный email', unique=True)
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comments = models.TextField(verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно')
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена')
    ]
    mailing_time = models.TimeField(verbose_name='Время рассылки')
    frequency = models.CharField(verbose_name='Периодичность', choices=FREQUENCY_CHOICES)
    mailing_status = models.CharField(verbose_name='Статус рассылки', choices=STATUS_CHOICES, default='created')

    clients = models.ManyToManyField(Client, verbose_name='Клиенты для рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, **NULLABLE, verbose_name='тема письма')

    def __str__(self):
        return f'{self.id}. Рассылка в {str(self.mailing_time)} - статус: {str(self.mailing_status)}.'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Отправлено'),
        ('failed', 'Не удалось отправить'),
        ('pending', 'В ожидании')
    ]
    time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(verbose_name='статус попытки', choices=STATUS_CHOICES)
    server_response = models.CharField(**NULLABLE, verbose_name='ответ почтового сервера')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, **NULLABLE, verbose_name='получатель')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
