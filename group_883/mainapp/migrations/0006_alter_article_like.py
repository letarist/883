# Generated by Django 4.0.3 on 2022-07-05 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_article_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='like',
            field=models.BigIntegerField(blank=True, default=0, verbose_name='Количество лайков'),
        ),
    ]
