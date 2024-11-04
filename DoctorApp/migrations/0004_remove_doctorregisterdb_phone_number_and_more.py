# Generated by Django 5.1 on 2024-09-25 17:56

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('DoctorApp', '0003_alter_doctorregisterdb_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorregisterdb',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='doctorregisterdb',
            name='availability',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='doctorregisterdb',
            name='location',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
        migrations.AddField(
            model_name='doctorregisterdb',
            name='password1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='doctorregisterdb',
            name='password2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='doctorregisterdb',
            name='submitted_on',
            field=models.DateField(default=datetime.date.today),

        ),
        migrations.AddField(
            model_name='doctorregisterdb',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
