# Generated by Django 3.1.14 on 2023-04-12 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0131_community_is_demo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CommunityTimeStamp',
            new_name='CommunitySnapshot',
        ),
        migrations.AlterModelTable(
            name='communitysnapshot',
            table='community_snapshots',
        ),
    ]
