# Generated by Django 5.1 on 2024-08-18 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContentDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(blank=True, null=True, upload_to='Content Images')),
                ('Title', models.CharField(blank=True, max_length=100, null=True)),
                ('ContentType', models.CharField(blank=True, max_length=50, null=True)),
                ('Content', models.TextField(blank=True, max_length=500, null=True)),
                ('Category', models.CharField(blank=True, max_length=50, null=True)),
                ('Author', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
