from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='social_dashboard'),
    path('add/', views.add_account, name='add_account'),
    path('update/<int:account_id>/', views.update_usage, name='update_usage'),
]
