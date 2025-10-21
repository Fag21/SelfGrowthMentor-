from django.urls import path
from . import views
app_name = 'growthfeed' 
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books/', views.book_section, name='book_section'),
    path('videos/', views.video_section, name='video_section'),
    path('actions/', views.actions, name='actions'),
    path('actions/exercise/', views.exercise, name='exercise'),
    path('actions/meditation/', views.meditation, name='meditation'),
    path('actions/custom_action/', views.custom_action, name='custom_action'),
    path('advices/', views.advice_list, name='advice_list'),           ]
