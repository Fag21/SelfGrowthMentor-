from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta, date
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Habit, HabitLog
from .forms import HabitForm, HabitQuickForm
from habits import models


# =====================
# DASHBOARD & CHART
# =====================

from django.utils import timezone
from django.db.models import Count, Q
from django.shortcuts import render
from .models import Habit, HabitLog
import json
from datetime import timedelta
@login_required
def habits_dashboard(request):
    user = request.user
    habits = Habit.objects.filter(user=user, active=True)
    
    # Get last 7 days
    today = timezone.localdate()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    # ✅ Use Q from django.db.models, not from habits.models
    logs = (
        HabitLog.objects.filter(habit__user=user, date__in=last_7_days)
        .values('date')
        .annotate(completed_count=Count('id', filter=Q(completed=True)))
    )

    # Build chart dataset
    log_dict = {entry['date']: entry['completed_count'] for entry in logs}
    chart_labels = [d.strftime("%a") for d in last_7_days]
    chart_values = [log_dict.get(d, 0) for d in last_7_days]

    chart_data = {
        'labels': chart_labels,
        'datasets': [{
            'label': 'Habits Completed',
            'data': chart_values,
            'borderColor': '#10B981',
            'backgroundColor': 'rgba(16, 185, 129, 0.2)',
            'fill': True,
            'tension': 0.4,
        }]
    }

    return render(request, 'habits/dashboard.html', {
        'habits': habits,
        'chart_data': json.dumps(chart_data),
    })

# =====================
# CRUD VIEWS
# =====================
@login_required
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, "Habit created — good luck! 🌱")
            return redirect('habits:dashboard')
    else:
        form = HabitForm(initial={'commitment': 5, 'goal_duration': 30})
    return render(request, 'habits/create_habit.html', {'form': form})


@login_required
def edit_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, "Habit updated")
            return redirect('habits:detail', pk=habit.pk)
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/edit_habit.html', {'form': form, 'habit': habit})


@login_required
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, "Habit deleted")
        return redirect('habits:dashboard')
    return render(request, 'habits/confirm_delete.html', {'habit': habit})


@login_required
def detail_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    quick_form = HabitQuickForm(instance=habit)
    logs = HabitLog.objects.filter(habit=habit).order_by('-date')[:10]
    return render(request, 'habits/detail.html', {
        'habit': habit,
        'quick_form': quick_form,
        'logs': logs
    })


# =====================
# COMPLETION LOGIC
# =====================
@login_required

@csrf_exempt
def toggle_completion(request, pk):
    """AJAX endpoint to toggle habit completion for today."""
    if request.method == "POST":
        try:
            habit = Habit.objects.get(pk=pk, user=request.user)
        except Habit.DoesNotExist:
            return JsonResponse({'error': 'Habit not found'}, status=404)

        today = timezone.localdate()
        log, created = HabitLog.objects.get_or_create(habit=habit, date=today)

        # Toggle completion
        log.completed = not log.completed
        log.save()

        if log.completed:
            habit.mark_complete()
        else:
            habit.reset_today()

        return JsonResponse({
            'success': True,
            'completed_today': habit.completed_today,
            'current_streak': habit.current_streak,
        })

    return JsonResponse({'error': 'Invalid method'}, status=400)
