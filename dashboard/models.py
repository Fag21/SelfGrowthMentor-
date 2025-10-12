from django.db import models
from django.contrib.auth.models import User

class DailyUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    screen_time_minutes = models.PositiveIntegerField(default=0)
    daily_limit_minutes = models.PositiveIntegerField(default=240)

    def remaining_time(self):
        return max(0, self.daily_limit_minutes - self.screen_time_minutes)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    streak_days = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class SocialMediaUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.platform}: {self.minutes}m"


class GrowthTip(models.Model):
    message = models.TextField()
    icon = models.CharField(max_length=10, default="🌱")
    ai_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.message[:40]
