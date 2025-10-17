from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Motive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    reward = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()
    progress = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def calculate_progress(self):
        total_days = (self.end_date - self.start_date).days
        elapsed_days = (date.today() - self.start_date).days
        if total_days > 0:
            self.progress = min(100, int((elapsed_days / total_days) * 100))
        if self.progress == 100 and not self.completed:
            self.completed = True
            self.xp += 50
        self.save()


class Biography(models.Model):
    name = models.CharField(max_length=100)
    short_intro = models.CharField(max_length=255)
    full_story = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('Business', 'Business'),
        ('Science', 'Science'),
        ('Sports', 'Sports'),
        ('Art', 'Art'),
        ('Technology', 'Technology'),
    ])
    image = models.ImageField(upload_to='biographies/', blank=True, null=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.text[:50]}..."


class VisionBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vision_board/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
