# Generated by Django 5.0.1 on 2024-07-14 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0043_config_success'),
    ]

    operations = [
        migrations.AlterField(
            model_name='success',
            name='success_value',
            field=models.BigIntegerField(default=0),
        ),
    ]
