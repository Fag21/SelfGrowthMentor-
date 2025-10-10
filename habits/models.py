from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import F

class Habit(models.Model):
    HABIT_TYPE_CHOICES = [
        ('build', 'Build'),
        ('quit', 'Quit'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=150)
    habit_type = models.CharField(max_length=10, choices=HABIT_TYPE_CHOICES)
    reason = models.TextField(blank=True)
    plan = models.TextField(blank=True, help_text="Describe when/where/how you'll do this habit")
    commitment = models.PositiveSmallIntegerField(default=5, help_text="1-10 scale")
    goal_duration = models.PositiveIntegerField(default=30, help_text="Goal duration in days")
    start_date = models.DateField(default=timezone.now)
    current_streak = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)
    completed_today = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_habit_type_display()})"

    def mark_complete(self, date=None):
        """Mark habit as completed for a day. Updates streaks and timestamps."""
        if date is None:
            date = timezone.localdate()
        # If last_completed is yesterday -> increment streak
        if self.last_completed:
            delta = (date - self.last_completed).days
            if delta == 1:
                self.current_streak = F('current_streak') + 1
            elif delta > 1:
                # break in streak
                self.current_streak = 1
        else:
            self.current_streak = 1

        # set last_completed, best_streak update will be applied after saving because F() used
        self.last_completed = date
        self.completed_today = True
        self.save()
        # refresh object to resolve F expression
        self.refresh_from_db()
        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak
            self.save()

    def reset_today(self):
        self.completed_today = False
        self.save()
