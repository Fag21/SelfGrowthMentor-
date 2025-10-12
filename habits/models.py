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
    plan = models.TextField(blank=True, help_text="Describe when, where, and how you'll do this habit")
    commitment = models.PositiveSmallIntegerField(default=5, help_text="Commitment level (1–10)")
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

    # ------------------------------
    # Core Logic
    # ------------------------------
    def mark_complete(self, date=None):
        """
        Mark this habit as completed for a given date (defaults to today).
        Updates streaks, best streak, and creates a log entry.
        """
        if date is None:
            date = timezone.localdate()

        # Skip if already logged today
        if self.last_completed == date:
            return

        # Handle streak logic
        if self.last_completed:
            gap = (date - self.last_completed).days
            if gap == 1:
                self.current_streak += 1
            elif gap > 1:
                self.current_streak = 1
        else:
            self.current_streak = 1

        # Update best streak if needed
        self.best_streak = max(self.best_streak, self.current_streak)

        # Update completion info
        self.last_completed = date
        self.completed_today = True
        self.save(update_fields=[
            'current_streak', 'best_streak', 'last_completed', 'completed_today', 'updated_at'
        ])

        # Ensure a log entry exists
        HabitLog.objects.get_or_create(
            habit=self, date=date, defaults={'completed': True}
        )

    def reset_today(self):
        """Mark the habit as not completed for today."""
        self.completed_today = False
        self.save(update_fields=['completed_today', 'updated_at'])

    def completion_rate(self, days=30):
        """
        Return completion rate (%) for the past N days.
        Example: habit.completion_rate(7) → last 7 days
        """
        today = timezone.localdate()
        start_date = today - timezone.timedelta(days=days - 1)
        total_days = days
        completed_days = self.logs.filter(date__range=(start_date, today), completed=True).count()
        return round((completed_days / total_days) * 100, 1)


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']

    def __str__(self):
        status = "✅ Done" if self.completed else "❌ Missed"
        return f"{self.habit.name} - {self.date} - {status}"
