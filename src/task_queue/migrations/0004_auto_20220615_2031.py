# Generated by Django 3.1.14 on 2022-06-15 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_queue', '0003_auto_20220612_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='job_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
