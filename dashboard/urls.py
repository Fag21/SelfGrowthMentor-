from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='index'),
    path('', views.social_data_api, name='social_data_api'),
    
]
