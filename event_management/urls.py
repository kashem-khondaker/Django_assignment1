from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/' , include("categories.urls") ),
    path('events/' , include("events.urls")),
    path('participants/' , include("Participants.urls")),
]
