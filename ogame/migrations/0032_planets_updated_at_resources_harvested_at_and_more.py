# Generated by Django 5.0.1 on 2024-01-28 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0031_alter_users_pseudo_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='planets',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=None, max_length=0, null=True),
        ),
        migrations.AddField(
            model_name='resources',
            name='harvested_at',
            field=models.DateTimeField(blank=True, default=None, max_length=0, null=True),
        ),
        migrations.AddField(
            model_name='resources',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=None, max_length=0, null=True),
        ),
    ]