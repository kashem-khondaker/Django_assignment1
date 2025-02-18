from django.contrib import admin
from django.urls import path , include
from .views import Home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',Home,name="home"),
    path('categories/' , include("categories.urls") ),
    path('events/' , include("events.urls")),
    path('participants/' , include("Participants.urls")),
]

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
