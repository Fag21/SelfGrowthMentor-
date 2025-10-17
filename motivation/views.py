from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Motive, Biography, Quote
from .forms import MotiveForm
import random
from .utils import fetch_random_quote, fetch_biography_from_wikipedia
from .models import Biography  # your local
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Motive
from .forms import MotiveForm

@login_required
def motivation_home(request):
    motives = Motive.objects.filter(user=request.user)
    for motive in motives:
        motive.calculate_progress()

    # Fetch a motivational quote
    try:
        quote_data = requests.get("https://zenquotes.io/api/random", timeout=5).json()[0]
        quote = quote_data["q"]
        author = quote_data["a"]
    except Exception as e:
        quote = "Keep pushing forward no matter what!"
        author = "Unknown"

    # Fetch biography (example: random successful person)
    try:
        bio_data = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/Elon_Musk", timeout=5).json()
        bio_title = bio_data["title"]
        bio_summary = bio_data["extract"]
        bio_image = bio_data.get("thumbnail", {}).get("source", "")
    except Exception as e:
        bio_title = "Elon Musk"
        bio_summary = "A visionary entrepreneur known for founding SpaceX, Tesla, and more."
        bio_image = ""

    return render(request, "motivation/motivation_home.html", {
        "motives": motives,
        "quote": quote,
        "author": author,
        "bio_title": bio_title,
        "bio_summary": bio_summary,
        "bio_image": bio_image,
    })


@login_required
def add_motive(request):
    if request.method == "POST":
        form = MotiveForm(request.POST)
        if form.is_valid():
            motive = form.save(commit=False)
            motive.user = request.user
            motive.save()
            return redirect("motivation_home")
    else:
        form = MotiveForm()
    return render(request, "motivation/add_motive.html", {"form": form})



@login_required
def complete_motive(request, motive_id):
    motive = get_object_or_404(Motive, id=motive_id, user=request.user)
    motive.completed = True
    motive.save()
    return redirect('motivation_home')
