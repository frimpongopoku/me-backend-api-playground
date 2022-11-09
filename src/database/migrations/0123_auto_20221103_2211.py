# Generated by Django 3.1.14 on 2022-11-03 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0122_auto_20221012_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customcommunitywebsitedomain',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='community_website', to='database.community'),
        ),
        migrations.AlterField(
            model_name='customcommunitywebsitedomain',
            name='website',
            field=models.URLField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subdomain_community', to='database.community'),
        ),
    ]
