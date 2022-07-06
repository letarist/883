# Generated by Django 4.0.3 on 2022-07-05 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_account', '0006_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(0, '@moderator'), (1, 'Like_Article'), (2, 'Comment'), (3, 'Like_Comment'), (4, 'Reply'), (5, 'Moderated')], verbose_name='Тип'),
        ),
    ]