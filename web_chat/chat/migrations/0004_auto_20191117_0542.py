# Generated by Django 2.2.6 on 2019-11-17 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20191114_0312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='room_id',
            new_name='thread',
        ),
    ]
