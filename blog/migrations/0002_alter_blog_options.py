# Generated by Django 4.2.1 on 2023-06-19 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'permissions': [('set_published_blog', 'Can publish blog')], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
    ]
