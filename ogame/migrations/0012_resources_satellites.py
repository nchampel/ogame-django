# Generated by Django 5.0 on 2024-01-03 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0011_buildings_fire_level_buildings_life_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resources',
            name='satellites',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
