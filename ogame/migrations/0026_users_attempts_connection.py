# Generated by Django 5.0 on 2024-01-13 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0025_token_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='attempts_connection',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
