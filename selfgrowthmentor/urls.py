from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('mentor/', include('mentor.urls')),
     path('journal/', include('journal.urls')),
    path('habits/', include(('habits.urls', 'habits'), namespace='habits')),

]
