# Generated by Django 3.1.14 on 2022-05-01 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_queue', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='recurring_interval',
            new_name='frequency',
        ),
    ]
