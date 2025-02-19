from django.shortcuts import render , redirect,get_object_or_404
from django.contrib import messages
from django.db.models import Q , Count
from events.forms import EventForm
from categories.forms import CategoriesForm
from categories.models import Categories
from Participants.models import Participant
from events.models import Event
from datetime import date,timezone
from django.contrib.auth.decorators import login_required , user_passes_test

def Event_view(request):
    return render(request, 'events/events.html')  

def is_organizer(user):
    return user.groups.filter(name__in=[ 'Organizer' ]).exists()
def is_organizer_or_admin(user):
    return user.groups.filter(name__in=[ 'Organizer' , 'Admin' ]).exists()


@user_passes_test(is_organizer_or_admin, login_url='no_permission')
def add_events(request):
    add_events_form = EventForm()
    if request.method == "POST":
        add_events_form = EventForm(request.POST , request.FILES)
        if add_events_form.is_valid():
            add_events_form.save()

            messages.success(request , "Event added successfully !")
            return redirect('Organizer_Dashboard')
        else:
            messages.error(request , "Something Went Wrong !")
            return redirect('add_event')
    context = { 'add_events_form':add_events_form}
    return render(request , 'events/create_event.html' , context)


@user_passes_test(is_organizer_or_admin, login_url='no_permission')
def update_events(request , id):
    event = Event.objects.get(id=id)
    event_form = EventForm(instance = event)
    event_categories_form = CategoriesForm(instance=event.category if event.category else None)

    if request.method == "POST":
        event_form = EventForm(request.POST, instance=event)
        event_categories_form = CategoriesForm(request.POST, instance=event.category if event.category else None)
        
        if event_form.is_valid() and event_categories_form.is_valid():
            events_categories = event_categories_form.save()
            events = event_form.save(commit=False)
            events.category = events_categories
            events.save()

            messages.success(request, "Event Update successfully !")
            return redirect('update_event', id=id )
    
    context = {
        'event_form':event_form,
        'event_categories_form': event_categories_form
    }

    return render(request , 'events/update_events.html' , context)


@user_passes_test(is_organizer_or_admin, login_url='no_permission')
def delete_events(request , id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()

        messages.success(request , "Event Deleted successfully !")
        return redirect('Organizer_Dashboard')
    else:
        messages.error(request, "Something Went Wrong !")
        return redirect('Organizer_Dashboard')




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


def Details(request, id):
    
    event = Event.objects.select_related('category').prefetch_related('participants').filter(id=id).first()
    participants = event.participants.all()
    
    context = {
        'event': event,
        'participants': participants, 
        'id': event.id,  
    }

    return render(request, 'Dashboard/details.html', context)


@login_required
@user_passes_test(is_organizer, login_url='log-in')
def Organizer_Dashboard(request):
    type = request.GET.get('type' , 'all')
    
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    
    participants = Participant.objects.distinct()
    categories = Categories.objects.all()
    total_participants = Participant.objects.aggregate(total=Count('id', distinct=True))
    total_participants_each_category = base_query.annotate(total_participants=Count('participants'))
    
    today_events = base_query.filter(date = date.today())
    today_events_participants = today_events.annotate(total_participants=Count('participants')).values('id', 'title', 'total_participants')
    
    events = base_query.none()

    if type == "Total_Participants":
        events = None
    elif type == "Total_Events":
        events = base_query.all()
    elif type == "Upcoming_Events":
        events = base_query.filter(date__gt = date.today())
    elif type == "Past_Events":
        events = base_query.filter(date__lt = date.today())
    elif type == "Today_Events":
        events = base_query.filter(date=date.today())

    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gt=date.today())),
        past_event=Count('id', filter=Q(date__lt=date.today())),
        Today_Events=Count('id', filter=Q(date=date.today()))
    )
    context = { 
        'events':events,
        'today_events':today_events,
        'today_events_participants':today_events_participants,
        'counts':counts,
        'participants':participants,
        'total_participants':total_participants,
        'total_participants_each_category':total_participants_each_category,
        'categories':categories,
    }
    return render(request, 'Dashboard/organizer_dashboard.html' , context)


@login_required
@user_passes_test(is_organizer_or_admin, login_url='no_permission')
def Search(request):
    query = request.GET.get('q', '')
    events = Event.objects.all()

    if query:
        events = events.filter(Q(title__icontains=query) | Q(location__icontains=query))
    
    context = {'events': events, 'query': query}

    return render(request, 'Dashboard/organizer_dashboard.html', context)


@login_required
@user_passes_test(is_organizer_or_admin, login_url='no_permission')
def Filter(request):
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = Event.objects.all()
    categories = Categories.objects.all()

    if category:
        events = events.filter(category_id=category)

    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, 'Dashboard/organizer_dashboard.html', {'events': events, "categories": categories})

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.rsvped_users.all():
        messages.warning(request, "You have already RSVP’d for this event.")
    else:
        event.rsvped_users.add(request.user)
        messages.success(request, "Successfully RSVP’d!")
    
    return redirect('participant_dashboard')