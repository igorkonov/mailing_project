from django.db import models
from mailing_app.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое статьи')
    picture = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение')
    views = models.IntegerField(verbose_name='Количество просмотров', default=0, **NULLABLE)
    published_on = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title
