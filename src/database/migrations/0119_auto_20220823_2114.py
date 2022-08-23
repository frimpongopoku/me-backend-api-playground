# Generated by Django 3.1.14 on 2022-08-23 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0118_feature_flags'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='is_approved',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_approved',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='vendor',
            name='is_approved',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
