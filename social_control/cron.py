from .models import SocialAccount
from datetime import timedelta
from django.utils import timezone
from .models import SocialPlatform


def reset_daily_usage():
    SocialAccount.objects.all().update(time_spent_today=0)
    print("✅ Daily social media usage reset done.")

def reset_daily_limits():
    today = timezone.now().date()
    platforms = SocialPlatform.objects.all()
    for platform in platforms:
        if platform.last_reset < today:
            platform.total_time_today = timedelta(0)
            platform.last_reset = today
            platform.save()
