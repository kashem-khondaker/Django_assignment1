from django.shortcuts import render , redirect
from django.contrib import messages
from events.forms import EventForm

def Event(request):
    return render(request, 'events/events.html')  


def add_events(request):
    add_events_form = EventForm()
    if request.method == "POST":
        add_events_form = EventForm(request.POST)
        if add_events_form.is_valid():
            add_events_form.save()

            messages.success(request , "Event added successfully !")
            return redirect('Events')
        else:
            messages.error(request , "Something Went Wrong !")
            return redirect('Events')
    context = { 'add_events_form':add_events_form}
    return render(request , 'events/create_event.html' , context)
        

