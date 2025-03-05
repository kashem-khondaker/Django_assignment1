from django.contrib import admin
from django.urls import path
from events.views import Home, Filter,rsvp_event,  add_events,Search,Organizer_Dashboard , update_events , delete_events , Details

urlpatterns = [
    # path('home' , Home , name='home'),
    path('create-event' , add_events , name="add_event"),
    path('update-event/<int:id>/' , update_events , name="update_event"),
    path('delete-event/<int:id>/' , delete_events , name="delete_events"),
    path('organizer-dashboard/',Organizer_Dashboard,name="Organizer_Dashboard"),
    path('search/',Search,name="Search"),
    path('filter/',Filter , name="filter"),
    path('details/<int:id>/',Details,name='Details'),
    path('rsvp/<int:event_id>/', rsvp_event, name='rsvp_event'),
]