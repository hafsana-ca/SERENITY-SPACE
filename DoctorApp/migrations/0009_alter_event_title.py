# Generated by Django 5.1 on 2024-09-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DoctorApp', '0008_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
