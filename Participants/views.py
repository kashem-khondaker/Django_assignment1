from django.shortcuts import render , redirect
from Participants.forms import ParticipantForm
from django.contrib import messages

def Participants(request):
    return render(request, 'Participants/participant_list.html')  

def Add_participants(request):
    add_participant = ParticipantForm()
    if request.method == "POST":
        add_participant = ParticipantForm(request.POST)
        if add_participant.is_valid():
            add_participant.save()
            
            messages.success(request , "Thank you for Participate !")
            return redirect('participant_list')
        else:
            messages.error(request, "Something Went Wrong , Please try again later !")
            return redirect('add_participant')
    context = {'add_participant':add_participant}
    return render(request , 'Participants/add_participants.html' , context)