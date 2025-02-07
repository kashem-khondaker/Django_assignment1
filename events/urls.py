from django.contrib import admin
from django.urls import path
from events.views import Events,Filter,  add_events,Search,Dashboard2 , Dashboard ,Organizer_Dashboard , update_events , delete_events

urlpatterns = [
    path('admin/' , admin.site.urls),
    path('create-event' , add_events , name="add_event"),
    path('update-event/<int:id>/' , update_events , name="update_event"),
    path('delete-event/<int:id>/' , delete_events , name="delete_events"),
    path('dashboard/',Dashboard,name="dashboard"),
    path('organizer-dashboard/',Organizer_Dashboard,name="Organizer_Dashboard"),
    path('search/',Search,name="Search"),
    path('dashboard2/',Dashboard2,name="dashboard2"),
    path('event-page/',Events , name="Events"),
    path('filter/',Filter , name="filter")
]