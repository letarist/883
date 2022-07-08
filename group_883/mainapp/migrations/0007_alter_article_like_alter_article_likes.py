# Generated by Django 4.0.3 on 2022-07-05 15:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0006_alter_article_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='like',
            field=models.BigIntegerField(default=0, verbose_name='Количество лайков'),
        ),
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]