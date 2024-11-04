from django.db import models

# Create your models here.

class ContentDB(models.Model):
    Image = models.ImageField(upload_to="Content Images", null=True, blank=True)
    Title = models.CharField(max_length=100, null=True, blank=True)
    ContentType = models.CharField(max_length=50, null=True, blank=True)
    Content = models.TextField(max_length=500, null=True, blank=True)
    Category = models.CharField(max_length=50, null=True, blank=True)
    Author = models.CharField(max_length=50, null=True, blank=True)


class MindfulnessExercise(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='mindfulness_covers/')
    media_file = models.FileField(upload_to='mindfulness_media/')  # For video/audio
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[('calm_music', 'Calm Music'), ('visualization_exercise', 'Visualization Exercise')])

    def __str__(self):
        return self.title



class MeditationSession(models.Model):
    DURATION_CHOICES = [
        (5, '5 minutes'),
        (10, '10 minutes'),
        (20, '20 minutes'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(choices=DURATION_CHOICES)
    media_type = models.CharField(max_length=10, choices=[('audio', 'Audio'), ('video', 'Video')])
    image = models.ImageField(upload_to='medi_images/', null=True, blank=True)
    media_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AromatherapySuggestion(models.Model):
    OIL_CHOICES = [
        ('Lavender', 'Lavender'),
        ('Eucalyptus', 'Eucalyptus'),
        ('Peppermint', 'Peppermint'),
        ('Chamomile', 'Chamomile'),
        ('Tea Tree', 'Tea Tree'),
        ('Rosemary', 'Rosemary'),
        ('Lemon', 'Lemon'),
        ('Cinnamon', 'Cinnamon'),
        ('Lemongrass', 'Lemongrass'),
        ('Clary sage', 'Clary sage'),
        ('Geranium', 'Geranium'),
        ('Roman chamomile', 'Roman chamomile'),
        ('Ylang-Ylang', 'Ylang-Ylang'),
        # Add more oils if needed
    ]

    oil_name = models.CharField(max_length=100, choices=OIL_CHOICES)
    benefits = models.TextField()
    description = models.TextField()
    usage_instructions = models.TextField()
    recommended_time = models.CharField(max_length=100)
    stress_level = models.CharField(max_length=100)
    image = models.ImageField(upload_to='aromatherapy_images/', blank=True, null=True)  # New image field

    def __str__(self):
        return f"{self.oil_name} - {self.recommended_time}"


DIFFICULTY_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]


class ExerciseRoutine(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  # Stretching, Yoga, Cardio, etc.
    target_areas = models.CharField(max_length=100,null=True)
    recommended_time = models.CharField(max_length=100,null=True)
    equipment = models.CharField(max_length=100,null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    instructions = models.TextField(help_text="Instructions or steps for the exercise")
    video_url = models.URLField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='exercise_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class GratitudePrompt(models.Model):
    prompt = models.TextField()
    challenge = models.TextField()
    entry_date = models.DateField(auto_now_add=True)
    week_number = models.IntegerField()

    def __str__(self):
        return f"Gratitude Prompt {self.id}"


class Challenge(models.Model):
    CHALLENGE_DURATION_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('multi-week', 'Multi-Week'),
        ('monthly', 'Monthly'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=20, choices=CHALLENGE_DURATION_CHOICES, default='daily')
    start_date = models.DateField()
    end_date = models.DateField()
    total_tasks = models.IntegerField()

    def __str__(self):
        return self.name


class NutritionalTip(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='nutritional_tips/', blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)  # Optional field for citation
    source_url = models.URLField(blank=True, null=True)  # Adding the URL field
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()  # Newline-separated list
    instructions = models.TextField()  # Step-by-step instructions
    nutrition_info = models.TextField()  # Calorie, protein info
    category = models.CharField(max_length=100)  # e.g., 'breakfast', 'vegan'
    preparation_time = models.IntegerField()  # Time in minutes
    health_benefit = models.TextField()  # Describes the health benefit of the recipe
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return self.title