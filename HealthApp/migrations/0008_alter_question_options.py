# Generated by Django 5.1 on 2024-09-24 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0007_question_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.JSONField(default=list),
        ),
    ]
