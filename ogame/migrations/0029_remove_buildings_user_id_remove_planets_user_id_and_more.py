# Generated by Django 5.0 on 2024-01-18 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0028_remove_resources_booster_remove_resources_crystal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildings',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='planets',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='planetsmultiverse',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='resources',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='searches',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='starship',
            name='user_id',
        ),
        migrations.AddField(
            model_name='buildings',
            name='users',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ogame.users'),
        ),
        migrations.AddField(
            model_name='planets',
            name='users',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ogame.users'),
        ),
        migrations.AddField(
            model_name='resources',
            name='harvestable',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='resources',
            name='users',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ogame.users'),
        ),
        migrations.AddField(
            model_name='searches',
            name='users',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ogame.users'),
        ),
        migrations.AddField(
            model_name='starship',
            name='users',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ogame.users'),
        ),
        migrations.AddField(
            model_name='users',
            name='nature',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
