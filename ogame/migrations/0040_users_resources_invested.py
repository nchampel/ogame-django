# Generated by Django 5.0.1 on 2024-07-12 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0039_users_unity_link_invested'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='resources_invested',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]