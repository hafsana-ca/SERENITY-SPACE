# Generated by Django 5.1 on 2024-10-16 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0033_challengeprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='gratitudeentry',
            name='challenge_completed',
            field=models.BooleanField(default=False),
        ),
    ]
