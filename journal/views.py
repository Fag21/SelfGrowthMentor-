from django.shortcuts import render, redirect, get_object_or_404

from selfgrowthmentor import settings
from .models import Journal
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
import json
from mentor.utils import get_ai_reflection

from django.shortcuts import render
from .models import Journal
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Journal
import google.generativeai as genai
from django.shortcuts import render
from .models import Journal

genai.configure(api_key="AIzaSyAvoEaywWZvObSVVYqbQdkVi4ZA5irtFtI")
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
# journal/views.py

def create_journal(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        journal = Journal.objects.create(user=request.user, title=title, content=content)

        # 💬 Get AI Reflection
        reflection = get_ai_reflection(content)
        journal.reflection = reflection
        journal.save()

        messages.success(request, "Journal added and mentor reflected 🌿")
        return redirect('dashboard')

    return render(request, 'journal/create_journal.html')



genai.configure(api_key=settings.GEMINI_API_KEY)

def read_journal(request, pk):
    journal = get_object_or_404(Journal, pk=pk)

    # Generate mentor reflection
    mentor_message = None
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are a gentle, wise AI mentor. Read this journal entry and give a 3–5 sentence reflection that feels kind, insightful, and motivating.
        Journal:
        {journal.content}
        """
        response = model.generate_content(prompt)
        mentor_message = response.text
    except Exception as e:
        mentor_message = "Your mentor is thinking deeply... please try again later."

    return render(request, "journal/read_journal.html", {
        "journal": journal,
        "mentor_message": mentor_message
    })



def delete_journal(request, pk):
    try:
        journal = Journal.objects.get(pk=pk)
    except Journal.DoesNotExist:
        messages.warning(request, "That journal was already released 🌬️")
        return redirect('dashboard')

    if request.method == "POST":
        journal.delete()
        messages.success(request, "Your journal has been released to the wind 🌬️")
        return redirect('dashboard')

    return redirect('read_journal', pk=pk)

