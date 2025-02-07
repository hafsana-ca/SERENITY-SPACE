# Generated by Django 5.1 on 2024-09-30 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0005_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='MindfulnessExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('cover_image', models.ImageField(upload_to='mindfulness_covers/')),
                ('media_file', models.FileField(upload_to='mindfulness_media/')),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('calm_music', 'Calm Music'), ('visualization_exercise', 'Visualization Exercise')], max_length=50)),
            ],
        ),
    ]
