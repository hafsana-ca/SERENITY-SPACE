# Generated by Django 5.1 on 2024-10-11 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0012_exerciseroutine_equipment'),
    ]

    operations = [
        migrations.CreateModel(
            name='GratitudePrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField()),
                ('challenge', models.TextField()),
                ('entry_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
