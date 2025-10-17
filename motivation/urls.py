from django.urls import path
from . import views
app_name = 'motivation'
urlpatterns = [
    path('', views.motivation_home, name='motivation_home'),
    path('add/', views.add_motive, name='add_motive'),
    path('complete/<int:motive_id>/', views.complete_motive, name='complete_motive'),
]
