# Generated by Django 5.1 on 2024-10-08 08:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0026_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitypost',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communitypost',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
