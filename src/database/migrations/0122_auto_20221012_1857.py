# Generated by Django 3.1.14 on 2022-10-12 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0121_media_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='communityadmingroup',
            options={'ordering': ['-id']},
        ),
    ]
