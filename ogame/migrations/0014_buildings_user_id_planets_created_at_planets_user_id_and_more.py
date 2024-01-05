# Generated by Django 5.0 on 2024-01-04 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0013_fight'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildings',
            name='user_id',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='planets',
            name='created_at',
            field=models.DateTimeField(blank=True, default=None, max_length=0, null=True),
        ),
        migrations.AddField(
            model_name='planets',
            name='user_id',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='planetsmultiverse',
            name='created_at',
            field=models.DateTimeField(blank=True, default=None, max_length=0, null=True),
        ),
        migrations.AddField(
            model_name='planetsmultiverse',
            name='user_id',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='resources',
            name='user_id',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
