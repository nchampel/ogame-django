# Generated by Django 5.0 on 2024-01-01 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0005_buildingsresources_resource_to_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildings',
            name='booster',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
