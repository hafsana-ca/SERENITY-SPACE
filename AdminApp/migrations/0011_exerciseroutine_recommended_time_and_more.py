# Generated by Django 5.1 on 2024-10-11 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0010_exerciseroutine'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseroutine',
            name='recommended_time',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='exerciseroutine',
            name='target_areas',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
