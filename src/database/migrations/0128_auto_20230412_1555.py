# Generated by Django 3.1.14 on 2023-04-12 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0127_auto_20230306_0944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ['rank', 'title']},
        ),
    ]
