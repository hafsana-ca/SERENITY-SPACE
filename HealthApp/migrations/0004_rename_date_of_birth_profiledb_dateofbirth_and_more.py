# Generated by Django 5.1 on 2024-09-18 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0003_profiledb'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profiledb',
            old_name='date_of_birth',
            new_name='DateOfBirth',
        ),
        migrations.RemoveField(
            model_name='profiledb',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profiledb',
            name='location',
        ),
        migrations.RemoveField(
            model_name='profiledb',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='profiledb',
            name='Image',
            field=models.ImageField(blank=True, null=True, upload_to='Profile Images/'),
        ),
        migrations.AddField(
            model_name='profiledb',
            name='Bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profiledb',
            name='Location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
