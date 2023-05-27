from django.db import models


from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    token = models.CharField(max_length=20, verbose_name='токен')
    token_time = models.DateTimeField(auto_now_add=True, verbose_name='время создания токена')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

