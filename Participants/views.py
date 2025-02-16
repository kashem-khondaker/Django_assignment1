from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib import messages
from Participants.forms import ParticipantForm
from Participants.models import Participant
from Participants.forms import RegistrationsForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required , user_passes_test




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
    


# Registrations for every participants

def User_Registrations(request):
    if request.method == 'POST' :
        form = RegistrationsForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # login(request , user)
            user = form.save(commit = False)
            user.is_active = False
            user.set_password(form.cleaned_data.get('password1'))

            messages.success(request , "User Registration successfully . Please check our email to activate your account ! ")
            return redirect('home') 
        
    else:
        form = RegistrationsForm()
    
    return render(request , 'Registrations/User_Sign_up.html' , {'form':form})




def User_Log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            messages.success(request, "Successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request , 'Registrations/User_Log_in.html')


@login_required
def User_Log_Out(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('log-in')
