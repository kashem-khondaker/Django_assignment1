from django.shortcuts import render , redirect
from django.contrib import messages
from Participants.forms import ParticipantForm
from Participants.models import Participant

def Participants(request):
    return render(request, 'Participants/participant_list.html')  

def Add_participants(request):
    add_participant = ParticipantForm()
    if request.method == "POST":
        add_participant = ParticipantForm(request.POST)
        if add_participant.is_valid():
            add_participant.save()
            
            messages.success(request , "Thank you for Participate !")
            return redirect('add_participant')
        else:
            messages.error(request, "Something Went Wrong , Please try again later !")
            return redirect('add_participant')
    context = {'add_participant':add_participant}
    return render(request , 'Participants/add_participants.html' , context)


def update_Participants(request , id):
    participant = Participant.objects.get(id=id)
    Participant_form = ParticipantForm(instance = participant)

    if request.method == "POST":
        Participant_form = ParticipantForm(request.POST, instance=participant)

        if Participant_form.is_valid() :
            
            participants = Participant_form.save(commit=False)
            participants.save()
            
            events = request.POST.getlist('events')
            participants.events.set(events)

            messages.success(request, "Participants Update successfully !")
            return redirect('Organizer_Dashboard')
    
    context ={
        'participant':participant,
        'Participant_form': Participant_form,
    }

    return render(request , 'Participants/update_participant.html' , context)

def delete_participant(request , id):
    if request.method == "POST":
        participant = Participant.objects.get(id=id)
        participant.delete()

        messages.success(request , "Participant Deleted successfully !")
        return redirect('Organizer_Dashboard')  
    else:
        messages.error(request, "Something Went Wrong !")
        return redirect('Organizer_Dashboard')