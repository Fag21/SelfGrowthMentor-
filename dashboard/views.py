from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    user = request.user
    context = {
        "username": user.username,
        "screen_time": "3h 25m",
        "daily_limit": "4h 00m",
        "time_left": "35m",
    }
    return render(request, 'dashboard/index.html', context)
