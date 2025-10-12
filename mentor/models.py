from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    focus_hours = models.FloatField(default=0)
    learning_hours = models.FloatField(default=0)
    mindset_score = models.IntegerField(default=5)  # 1-10 scale
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    entry = models.TextField()
    mentor_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Journal {self.date}"



    def __str__(self):
        return f"{self.user.username} - {self.role}"
  

