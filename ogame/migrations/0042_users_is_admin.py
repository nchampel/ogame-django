# Generated by Django 5.0.1 on 2024-07-13 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0041_alter_users_resources_invested'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_admin',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
    ]