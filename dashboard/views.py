from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import DailyUsage, Habit, SocialMediaUsage, GrowthTip
import random
# dashboard/views.py
from django.shortcuts import render
from habits.models import Habit, HabitLog
from datetime import date, timedelta
from habits.views import habits_dashboard
def get_streak(habit):
    """Calculate current streak for a habit"""
    streak = 0
    today = date.today()
    day = today

    while True:
        if HabitLog.objects.filter(habit=habit, date=day, completed=True).exists():
            streak += 1
            day -= timedelta(days=1)
        else:
            break
    return streak



@login_required
def dashboard_view(request):
    user = request.user

    usage = DailyUsage.objects.filter(user=user).order_by('-date').first()
    if not usage:
        usage = DailyUsage.objects.create(user=user, screen_time_minutes=180)

    habits = Habit.objects.all()

    # Generate habit streaks
    streaks = [
        {"name": h.name, "streak": get_streak(h)} for h in habits
    ]

    # Sort by highest streak
    streaks.sort(key=lambda x: x["streak"], reverse=True)

    context = {
        "streaks": streaks,
    }
    tips = GrowthTip.objects.all()
    if not tips.exists():
        tips = [
            GrowthTip(message="✨ Focus on one calm deep work session today."),
            GrowthTip(message="🔥 You’re on a 7-day streak — keep your roots strong!"),
            GrowthTip(message="💡 Reflect on how you grew your mindset this week."),
        ]
        GrowthTip.objects.bulk_create(tips)
        tips = GrowthTip.objects.all()

    # For AI Mentor
    ai_messages = [
        "🌿 Your growth starts with one focused action today.",
        "💫 Remember: Progress > Perfection.",
        "🔥 You’ve been consistent — today’s your momentum day!",
        "🌻 Reflect 10 minutes before bed — that’s where wisdom grows.",
    ]
    daily_ai_tip = random.choice(ai_messages)

    context = {
        "usage": usage,
        "habits": habits,
        "tips": tips,
        "ai_tip": daily_ai_tip,
    }
    return render(request, "dashboard/index.html", context)


@login_required
def social_data_api(request):
    """Return user’s social media usage data as JSON for Chart.js"""
    user = request.user
    usage_data = SocialMediaUsage.objects.filter(user=user)
    if not usage_data.exists():
        default_data = [
            ("Instagram", 120),
            ("YouTube", 90),
            ("TikTok", 60),
            ("Twitter", 45),
            ("Facebook", 30)
        ]
        for platform, minutes in default_data:
            SocialMediaUsage.objects.create(user=user, platform=platform, minutes=minutes)
        usage_data = SocialMediaUsage.objects.filter(user=user)

    data = {
        "labels": [d.platform for d in usage_data],
        "values": [d.minutes for d in usage_data],
    }
    return JsonResponse(data)
