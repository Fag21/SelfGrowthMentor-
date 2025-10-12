from django.urls import path
from . import views

urlpatterns = [
    path('ai-chat/', views.ai_mentor_chat, name='ai_mentor_chat'),
]
