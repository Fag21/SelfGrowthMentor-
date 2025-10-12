from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('', views.habits_dashboard, name='dashboard'),
    path('create/', views.create_habit, name='create'),
    path('<int:pk>/', views.detail_habit, name='detail'),
    path('<int:pk>/edit/', views.edit_habit, name='edit'),
    path('<int:pk>/delete/', views.delete_habit, name='delete'),
    path('<int:pk>/toggle/', views.toggle_completion, name='toggle_completion'),
    
]
