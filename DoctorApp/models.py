from django.db import models
import datetime

class DoctorRegisterDB(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20,null=True, blank=True)
    location = models.CharField(max_length=220,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='doctor_pics/')
    specialization = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100)
    qualification = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    password1 = models.CharField(max_length=255,null=True, blank=True)
    password2 = models.CharField(max_length=255, null=True, blank=True)
    availability = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField()
    is_approved = models.BooleanField(default=False)  # Status for admin approval
    submitted_on = models.DateField(null=True, blank=True, default=datetime.date.today)

    # Status for admin approval

    def __str__(self):
        return self.name



class Event(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    organizer = models.CharField(max_length=100)
    organizer_info = models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField()
    cover_image = models.ImageField(upload_to='event_images/')  # Event cover image

    def __str__(self):
        return self.title

