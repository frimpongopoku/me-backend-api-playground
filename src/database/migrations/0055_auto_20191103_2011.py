# Generated by Django 2.2.5 on 2019-11-03 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0054_auto_20191102_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='owner_phone_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
