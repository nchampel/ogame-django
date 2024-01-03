# Generated by Django 5.0 on 2023-12-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metal', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(max_length=0)),
            ],
            options={
                'db_table': 'resources',
            },
        ),
    ]
