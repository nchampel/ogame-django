# Generated by Django 5.0 on 2024-01-13 13:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogame', '0024_searches_crystal_searches_deuterium_searches_metal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, max_length=0, null=True)),
            ],
            options={
                'db_table': 'token',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pseudo', models.BooleanField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(max_length=0)),
                ('last_login', models.DateTimeField(blank=True, default=None, max_length=0, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
