# Generated by Django 3.1.12 on 2021-08-26 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0103_auto_20210826_1104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carbonequivalency',
            options={'ordering': ('id',), 'verbose_name_plural': 'CarbonEquivalencies'},
        ),
        migrations.AlterModelTable(
            name='carbonequivalency',
            table='carbon_equivalencies',
        ),
    ]
