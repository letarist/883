# Generated by Django 4.0.3 on 2022-07-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_article_moderated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='like',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Количество лайков'),
        ),
    ]