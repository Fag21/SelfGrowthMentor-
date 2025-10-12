from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'habit_type', 'current_streak', 'best_streak', 'active', 'start_date')
    list_filter = ('habit_type', 'active')
    search_fields = ('name', 'user__username')
