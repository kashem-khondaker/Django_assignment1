from django.contrib import admin
from django.urls import path , include
from .views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',Home,name="home"),
    path('categories/' , include("categories.urls") ),
    path('events/' , include("events.urls")),
    path('participants/' , include("Participants.urls")),
]
