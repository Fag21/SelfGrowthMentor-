from django.shortcuts import render, redirect, get_object_or_404
from .models import Journal
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render
from .models import Journal
from datetime import date, timedelta
@login_required
def dashboard(request):
    journals = Journal.objects.filter(user=request.user).order_by('-date')
    last_7_days = date.today() - timedelta(days=6)
    recent_journals = journals.filter(date__gte=last_7_days)

    # prepare chart data
    chart_labels = [j.date.strftime('%Y-%m-%d') for j in recent_journals]
    chart_data = [1 for _ in recent_journals]

    context = {
        'recent_journals': recent_journals,
        'old_journals': journals.exclude(date__gte=last_7_days),
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'journal/dashboard.html', context)


@login_required
def create_journal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        mood = request.POST.get('mood')
        Journal.objects.create(user=request.user, title=title, content=content, mood=mood)
        return redirect('dashboard')
    return render(request, 'journal/create_journal.html')

@login_required
def read_journal(request, pk):
    journal = get_object_or_404(Journal, id=pk, user=request.user)
    return render(request, 'journal/read_journal.html', {'journal': journal})
