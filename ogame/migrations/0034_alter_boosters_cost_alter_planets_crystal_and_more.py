# Generated by Django 5.0.1 on 2024-02-03 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0033_rename_deuterium_buildingsresources_tritium_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boosters',
            name='cost',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='planets',
            name='crystal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='planets',
            name='metal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='planets',
            name='tritium',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='planetsmultiverse',
            name='crystal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='planetsmultiverse',
            name='metal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='planetsmultiverse',
            name='tritium',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='resources',
            name='resource_value',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='searches',
            name='crystal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='searches',
            name='metal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='searches',
            name='tritium',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
