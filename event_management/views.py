from django.shortcuts import render , redirect
from django.contrib import messages
from django.db.models import Q , Count
from events.forms import EventForm
from categories.forms import CategoriesForm
from categories.models import Categories
from Participants.models import Participant
from events.models import Event
from datetime import date,timezone

def Home(request):
    type = request.GET.get('type', 'all')

    base_query = Event.objects.select_related('category').prefetch_related('participants').all()

    Total_Participants = {'total': 0}
    events = base_query.none()

    if type == "Total_Participants":
        Total_Participants = Participant.objects.aggregate(total=Count('id', distinct=True))
    elif type == "Total_Events":
        events = base_query.all()
    elif type == "Upcoming_Events":
        events = base_query.filter(date__gt=date.today())
    elif type == "Past_Events":
        events = base_query.filter(date__lt=date.today())
    elif type == "Today_Events":
        events = base_query.filter(date__date=date.today())

    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gt=date.today())),
        past_event=Count('id', filter=Q(date__lt=date.today())),
    )

    # Fetch the participant count for each event
    for event in events:
        event.total_participants = event.participants.count()

    context = {
        'events': events,
        'counts': counts,
        'Total_Participant': Total_Participants
    }
    return render(request, 'Dashboard/home.html', context)
