from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SocialAccount(models.Model):
    PLATFORM_CHOICES = [
        ('YouTube', 'YouTube'),
        ('Instagram', 'Instagram'),
        ('TikTok', 'TikTok'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    daily_limit_minutes = models.PositiveIntegerField(default=60)
    time_spent_today = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def is_over_limit(self):
        return self.time_spent_today >= self.daily_limit_minutes

    def __str__(self):
        return f"{self.user.username} - {self.platform}"
from django.utils import timezone

class SocialSession(models.Model):
    account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    def get_duration_minutes(self):
        end = self.end_time or timezone.now()
        return int((end - self.start_time).total_seconds() / 60)
