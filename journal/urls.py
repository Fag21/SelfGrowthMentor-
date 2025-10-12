from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('write/', views.create_journal, name='create_journal'),
    path('read/<int:pk>/', views.read_journal, name='read_journal'),
]
