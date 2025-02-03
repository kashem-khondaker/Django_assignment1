from django.contrib import admin
from django.urls import path
from events.views import Event , add_events

urlpatterns = [
    path('admin/' , admin.site.urls),
    path('' ,Event ,name="Events"),
    path('create-event' , add_events),
]