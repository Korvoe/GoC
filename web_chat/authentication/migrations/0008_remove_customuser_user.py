# Generated by Django 2.2.6 on 2019-11-13 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20191113_0753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user',
        ),
    ]
