from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from datetime import date
import uuid
from datetime import datetime
from django.utils import timezone
from DoctorApp.models import Event, DoctorRegisterDB
from AdminApp.models import ExerciseRoutine, GratitudePrompt, Challenge

class ContactDB(models.Model):
    Name = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=50, null=True, blank=True)
    Message = models.TextField(max_length=500, null=True, blank=True)

class RegisterDB(models.Model):
    Username = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=50,null=True,blank=True)
    Password1 = models.CharField(max_length=50,null=True,blank=True)
    Password2 = models.CharField(max_length=50,null=True,blank=True)
    Image = models.ImageField(upload_to="Register Images", null=True, blank=True)


class ProfileDB(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Bio = models.TextField(null=True, blank=True)
    DateOfBirth = models.DateField(null=True, blank=True)
    Location = models.CharField(max_length=255, null=True, blank=True)
    Image = models.ImageField(upload_to='Profile Images/', null=True, blank=True)

    def __str__(self):
        return self.user.username



class JournalEntry(models.Model):
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    mood = models.CharField(max_length=10, choices=[
        ('😊', 'Happy'),
        ('😔', 'Sad'),
        ('😡', 'Angry'),
        ('😎', 'Excited'),
        ('😌', 'Calm')
    ])
    image = models.ImageField(upload_to='journal_images/', null=True, blank=True)
    date_created = models.DateField(default=date.today)

    class Meta:
        unique_together = ('user', 'date_created')

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField(default=list)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.options:
            self.options = ['Not at all', 'Several Days', 'more than half the days', 'Always']
        super().save(*args, **kwargs)



class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_response = models.CharField(max_length=255)
    stress_level = models.IntegerField()
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    screening_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Use UUIDField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.question} - {self.stress_level}'




class Appointment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    age = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField()
    doctor = models.ForeignKey(DoctorRegisterDB, on_delete=models.CASCADE, default=1)  # Use the ID of a doctor as the default




class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)  # Username from session
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    booking_date = models.DateTimeField(auto_now_add=True)  # Automatically set the booking date

    def __str__(self):
        return f"Booking by {self.username} for {self.event.title}"


class CommunityPost(models.Model):
    author = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)  # Link to the user who posted
    title = models.CharField(max_length=200, null=True, blank=True)  # Add title field for the post
    text = models.TextField(max_length=500)  # The post content
    image = models.ImageField(upload_to='community_images/', blank=True, null=True)  # Optional image
    votes = models.IntegerField(default=0)  # Field to store the number of votes
    created_at = models.DateTimeField(default=timezone.now)  # Use timezone-aware datetime

    def __str__(self):
        return self.title  # Change string representation to show the title



class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=300)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.author.username} - {self.comment_text[:30]}'

class Reply(models.Model):
    post = models.ForeignKey(CommunityPost, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    reply_text = models.TextField(max_length=300)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.author.username} - {self.reply_text[:30]}'



class PostVote(models.Model):
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # Ensures one like per user per post


class ExerciseLog(models.Model):
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)  # Referencing your custom user model
    exercise = models.ForeignKey(ExerciseRoutine, on_delete=models.CASCADE)
    date_completed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.Username} - {self.exercise.name}"  # Assuming RegisterDB has a field 'Username'



class GratitudeEntry(models.Model):
    prompt = models.ForeignKey(GratitudePrompt, on_delete=models.CASCADE)
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)  # Link to your custom user model
    entry_text = models.TextField()
    entry_date = models.DateField(auto_now_add=True)
    challenge_completed = models.BooleanField(default=False)  # New field to track challenge completion

    def __str__(self):
        return f"Gratitude Entry by {self.user.Username} on {self.entry_date}"



class ChallengeProgress(models.Model):
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)  # Links to admin-side challenge
    date = models.DateField()  # Date user completed the task
    completed = models.BooleanField(default=False)  # Tracks if user completed task
    completion_date = models.DateField(null=True, blank=True)  # Optional field to track when the challenge was completed

    def save(self, *args, **kwargs):
        if self.completed:
            self.completion_date = timezone.now().date()  # Set the completion date when task is marked completed
        else:
            self.completion_date = None  # Reset if not completed
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.Username} - {self.challenge.name} - {self.date}"
