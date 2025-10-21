from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils import timezone



# ----------------- BOOK MODEL -----------------
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    cover_image = models.URLField(blank=True, null=True)
    file_url = models.URLField(null=True, blank=True)


    category = models.CharField(max_length=100, default="Self Development")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ----------------- VIDEO MODEL -----------------
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    youtube_url = models.URLField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, default="Self Development")
    created_at = models.DateTimeField(default=timezone.now)
 


    def __str__(self):
        return self.title


# ----------------- USER PROGRESS MODEL -----------------
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books_read = models.ManyToManyField(Book, blank=True)
    videos_watched = models.ManyToManyField(Video, blank=True)
    last_read = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True, related_name="last_read_by"
    )
    performance_score = models.IntegerField(default=0)  # will be shown as chart

    def __str__(self):
        return f"{self.user.username} Progress"


# ----------------- ACTION MODEL -----------------
class Action(models.Model):
    ACTION_TYPES = [
        ('exercise', 'Exercise'),
        ('meditation', 'Meditation'),
        ('custom', 'Custom'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type}"


# ----------------- AI ADVICE MODEL -----------------
class AIAdvice(models.Model):
    CATEGORY_CHOICES = [
        ('mindset', 'Mindset'),
        ('productivity', 'Productivity'),
        ('discipline', 'Discipline'),
        ('emotional', 'Emotional Growth'),
        ('spiritual', 'Spiritual'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.title()} advice - {self.text[:50]}"


# ----------------- FAVORITE MODEL -----------------
class Favorite(models.Model):
    FAVORITE_TYPE_CHOICES = [
        ('book', 'Book'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_type = models.CharField(max_length=10, choices=FAVORITE_TYPE_CHOICES)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'favorite_type', 'book', 'video')

    def __str__(self):
        if self.favorite_type == 'book' and self.book:
            return f"{self.user.username} - {self.book.title}"
        elif self.favorite_type == 'video' and self.video:
            return f"{self.user.username} - {self.video.title}"
        return f"{self.user.username} - Unknown"
