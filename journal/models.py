from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

MOOD_CHOICES = [
    ('happy', '😊 Happy'),
    ('calm', '😌 Calm'),
    ('sad', '😢 Sad'),
    ('angry', '😡 Angry'),
    ('motivated', '💪 Motivated'),
]

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='calm')
    reflection = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.date})"

    @staticmethod
    def current_streak(user):
        journals = Journal.objects.filter(user=user).order_by('-date')
        streak = 0
        today = date.today()
        for j in journals:
            if (today - j.date).days == streak:
                streak += 1
            else:
                break
        return streak
