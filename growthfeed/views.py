from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
import random

from .models import (
    Book,
    Video,
    UserProgress,
    AIAdvice,
    Action,
    Favorite,
)


# ----------------- DASHBOARD VIEW -----------------
@login_required
def dashboard(request):
    user = request.user

    # Get or create user progress
    progress, _ = UserProgress.objects.get_or_create(user=user)

    # 🧠 AI Advice Section
    advice_queryset = AIAdvice.objects.all()
    advice = advice_queryset.order_by('-created_at').first() if advice_queryset.exists() else None
    advice_text = advice.text if advice else "Keep growing every day — small progress adds up to big change!"

    # 📚 Books Section
    last_read = progress.last_read
    favorite_books = progress.books_read.all()[:2]  # last 2 books read
    all_books = [book for book in [last_read, *favorite_books] if book]

    # 🎥 Videos Section
    last_videos = progress.videos_watched.all()[:3]

    # ⚡ Actions Section
    user_actions = Action.objects.filter(user=user).order_by('-created_at')[:3]

    # 📈 Chart Data (placeholder)
    chart_data = {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "values": [60, 70, 80, 75, 90, 95, 100],
    }

    context = {
        "advice": advice_text,
        "books": all_books,
        "videos": last_videos,
        "chart_data": chart_data,
        "actions": user_actions,
    }

    return render(request, "growthfeed/dashboard.html", context)


# ----------------- ACTIONS VIEW -----------------
@login_required
def actions(request):
    user = request.user

    if request.method == "POST":
        action_type = request.POST.get("action_type")
        description = request.POST.get("description")
        Action.objects.create(user=user, action_type=action_type, description=description)
        return redirect("actions")

    actions = Action.objects.filter(user=user).order_by("-created_at")

    return render(request, "growthfeed/actions.html", {"actions": actions})


# ----------------- SUB ACTION PAGES -----------------
@login_required
def meditation(request):
    return render(request, "growthfeed/meditation.html")


@login_required
def exercise(request):
    return render(request, "growthfeed/exercise.html")


@login_required
def custom_action(request):
    user = request.user

    if request.method == "POST":
        description = request.POST.get("description")
        Action.objects.create(user=user, action_type="custom", description=description)
        return redirect("actions")

    return render(request, "growthfeed/custom_action.html")


# ----------------- AI ADVICE LIST VIEW -----------------
@login_required
def advice_list(request):
    category = request.GET.get("category", "all")
    if category == "all":
        advices = AIAdvice.objects.order_by("-created_at")
    else:
        advices = AIAdvice.objects.filter(category=category).order_by("-created_at")

    categories = AIAdvice.CATEGORY_CHOICES

    context = {
        "advices": advices,
        "categories": categories,
        "selected_category": category,
    }
    return render(request, "growthfeed/advice_list.html", context)


# ----------------- BOOK SECTION -----------------
@login_required
def book_section(request):
    query = request.GET.get("q", "")
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all().order_by("-created_at")

    context = {"books": books, "query": query}
    return render(request, "growthfeed/book_section.html", context)


# ----------------- VIDEO SECTION -----------------
@login_required
def video_section(request):
    query = request.GET.get("q", "")
    if query:
        videos = Video.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        videos = Video.objects.all().order_by("-created_at")

    context = {"videos": videos, "query": query}
    return render(request, "growthfeed/video_section.html", context)


# ----------------- TOGGLE FAVORITE (AJAX) -----------------
@login_required
def toggle_favorite(request):
    if request.method == "POST":
        user = request.user
        favorite_type = request.POST.get("type")
        item_id = request.POST.get("id")

        if favorite_type == "book":
            book = Book.objects.get(id=item_id)
            favorite, created = Favorite.objects.get_or_create(user=user, favorite_type="book", book=book)
            if not created:
                favorite.delete()
                return JsonResponse({"status": "removed"})

        elif favorite_type == "video":
            video = Video.objects.get(id=item_id)
            favorite, created = Favorite.objects.get_or_create(user=user, favorite_type="video", video=video)
            if not created:
                favorite.delete()
                return JsonResponse({"status": "removed"})

        return JsonResponse({"status": "added"})
