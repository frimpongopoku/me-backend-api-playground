# Generated by Django 3.1.14 on 2022-02-16 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0112_auto_20211221_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='is_external_event',
            new_name='rsvp_enabled',
        ),
    ]
