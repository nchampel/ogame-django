# Generated by Django 5.0 on 2023-12-30 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resources',
            name='crystal',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='resources',
            name='deuterium',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
