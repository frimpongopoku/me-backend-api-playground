# Generated by Django 3.0.14 on 2021-06-21 19:08

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0091_userprofile_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='color',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferences',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'color': '#000000'}, null=True),
        ),
    ]