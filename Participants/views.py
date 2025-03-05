from django.shortcuts import render , redirect,HttpResponse , get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User , Group
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib import messages
from Participants.forms import ParticipantForm,AssignedRoleForm , CreateGroupForm,ProfileCreate_Update_Form , CustomPasswordResetConfirmForm , CustomPasswordResetForm
from Participants.models import Participant , Profile
from Participants.forms import RegistrationsForm , ProfileCreate_Update_Form
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required , user_passes_test
from events.models import Event
from django.db.models import Q , Count
from categories.models import Categories
from datetime import date,timezone
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.utils.decorators import method_decorator





User = get_user_model()


def is_admin_or_organizer(user):
    return user.groups.filter(name__in=['Admin', 'Organizer']).exists()

def no_permission(request):
    return render(request , 'Admin/no_permission.html')

@user_passes_test(is_admin_or_organizer, login_url='no_permission')
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


@user_passes_test(is_admin_or_organizer, login_url='no_permission')
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
    
    context = {
        'participant':participant,
        'Participant_form': Participant_form,
    }

    return render(request , 'Participants/update_participant.html' , context)



@user_passes_test(is_admin_or_organizer, login_url='no_permission')
def delete_participant(request , id):
    if request.method == "POST":
        participant = Participant.objects.get(id=id)
        participant.delete()

        messages.success(request , "Participant Deleted successfully !")
        return redirect('dashboard')  
    else:
        messages.error(request, "Something Went Wrong !")
        return redirect('dashboard')
    


# Registrations for every participants
"""

def User_Registrations(request):
    if request.method == 'POST' :
        form = RegistrationsForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            messages.success(request , "User Registration successfully . Please check our email to activate your account ! ")
            return redirect('home') 
        
    else:
        form = RegistrationsForm()
    
    return render(request , 'Registrations/User_Sign_up.html' , {'form':form})

"""



class User_Registrations(View):

    template_name = 'Registrations/User_Sign_up.html'
    
    def get(self, request):
        form = RegistrationsForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = RegistrationsForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            
            messages.success(request, "User Registration successfully. Please check your email to activate your account!")
            return redirect('home')
        
        return render(request, self.template_name, {'form': form})


def activate_account(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "Your account has been activated successfully! You can now log in.")
            return redirect('log-in')
        else:
            messages.error(request, "Invalid activation link or token has expired.")
            return redirect('sign-up')

    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('sign-up')


"""

def User_Log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            messages.success(request, "Successfully logged in!")

            # Redirect based on user's group
            if user.groups.filter(name='User').exists():
                return redirect('participant_dashboard')  # Redirect to Admin dashboard
            if user.groups.filter(name='Admin').exists():
                return redirect('Admin_dashboard')  # Redirect to Admin dashboard
            elif user.groups.filter(name='Organizer').exists():
                return redirect('Organizer_Dashboard')  # Redirect to Manager dashboard
            else:
                return redirect('home') 

        else:
            messages.error(request, "Invalid username or password!")

    return render(request , 'Registrations/User_Log_in.html')

"""




class User_Log_in(LoginView):
    template_name = 'Registrations/User_Log_in.html'
    redirect_authenticated_user = True  

    def get_success_url(self):
        next_url = self.request.GET.get('next')  
        if next_url:
            return next_url  

        user = self.request.user  
        if user.is_authenticated:
            if user.groups.filter(name='Admin').exists():
                return reverse_lazy('Admin_dashboard')  # Admin Dashboard
            elif user.groups.filter(name='Organizer').exists():
                return reverse_lazy('Organizer_Dashboard')  # Organizer Dashboard
            elif user.groups.filter(name='User').exists():
                return reverse_lazy('participant_dashboard')  # Participant Dashboard

        return reverse_lazy('home')  

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password!")
        return super().form_invalid(form)



"""

class User_Log_in(View):

    def get(self , request):
        return render(request , 'Registrations/User_Log_in.html')
    
    def post(self , request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            messages.success(request, "Successfully logged in!")

            # Redirect based on user's group
            if user.groups.filter(name='User').exists():
                return redirect('participant_dashboard')  # Redirect to Admin dashboard
            if user.groups.filter(name='Admin').exists():
                return redirect('Admin_dashboard')  # Redirect to Admin dashboard
            elif user.groups.filter(name='Organizer').exists():
                return redirect('Organizer_Dashboard')  # Redirect to Manager dashboard
            else:
                return redirect('home') 

        else:
            messages.error(request, "Invalid username or password!")

        return render(request , 'Registrations/User_Log_in.html')

"""


# @login_required
# def User_Log_Out(request):
#     logout(request)
#     return redirect('home')


class User_Log_Out(LogoutView):
    
    next_page = 'home'



def is_admin(user):
    return user.groups.filter(name='Admin').exists()


@login_required
@user_passes_test(is_admin , login_url='no_permission')
def admin_dashboard(request):
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
    users = User.objects.all()
    total_users = User.objects.count()
    context = {
        'events':events,
        'users':users,
        'total_users':total_users,
        'today_events':today_events,
        'today_events_participants':today_events_participants,
        'counts':counts,
        'participants':participants,
        'total_participants':total_participants,
        'total_participants_each_category':total_participants_each_category,
        'categories':categories,
    }
    return render(request , 'Admin/admin_dashboard.html' , context)


def all_event(request):
    type = request.GET.get('type', 'all') 
    
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    
    participants = Participant.objects.distinct()
    categories = Categories.objects.all()
    total_participants = Participant.objects.aggregate(total=Count('id', distinct=True))
    total_participants_each_category = base_query.annotate(total_participants=Count('participants'))
    
    today_events = base_query.filter(date=date.today())
    today_events_participants = today_events.annotate(total_participants=Count('participants')).values('id', 'title', 'total_participants')

    # Ensure events always has a valid queryset
    events = base_query.all()  # Default: Show all events

    if type == "Total_Events":
        events = base_query.all()
    elif type == "Upcoming_Events":
        events = base_query.filter(date__gt=date.today())
    elif type == "Past_Events":
        events = base_query.filter(date__lt=date.today())
    elif type == "Today_Events":
        events = base_query.filter(date=date.today())

    # Count statistics
    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gt=date.today())),
        past_event=Count('id', filter=Q(date__lt=date.today())),
        Today_Events=Count('id', filter=Q(date=date.today()))
    )

    users = User.objects.all()
    total_users = User.objects.count()

    context = {
        'events': events,  # Ensure events is always a queryset
        'users': users,
        'total_users': total_users,
        'today_events': today_events,
        'today_events_participants': today_events_participants,
        'counts': counts,
        'participants': participants,
        'total_participants': total_participants,
        'total_participants_each_category': total_participants_each_category,
        'categories': categories,
    }
    
    return render(request, 'Admin/all_events.html', context)


def User_history(request):
    type = request.GET.get('type', 'all') 
    
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    
    participants = Participant.objects.distinct()
    categories = Categories.objects.all()
    total_participants = Participant.objects.aggregate(total=Count('id', distinct=True))
    total_participants_each_category = base_query.annotate(total_participants=Count('participants'))
    
    today_events = base_query.filter(date=date.today())
    today_events_participants = today_events.annotate(total_participants=Count('participants')).values('id', 'title', 'total_participants')

    # Ensure events always has a valid queryset
    events = base_query.all()  # Default: Show all events

    if type == "Total_Events":
        events = base_query.all()
    elif type == "Upcoming_Events":
        events = base_query.filter(date__gt=date.today())
    elif type == "Past_Events":
        events = base_query.filter(date__lt=date.today())
    elif type == "Today_Events":
        events = base_query.filter(date=date.today())

    # Count statistics
    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gt=date.today())),
        past_event=Count('id', filter=Q(date__lt=date.today())),
        Today_Events=Count('id', filter=Q(date=date.today()))
    )

    users = User.objects.all()
    total_users = User.objects.count()

    context = {
        'events': events,  # Ensure events is always a queryset
        'users': users,
        'total_users': total_users,
        'today_events': today_events,
        'today_events_participants': today_events_participants,
        'counts': counts,
        'participants': participants,
        'total_participants': total_participants,
        'total_participants_each_category': total_participants_each_category,
        'categories': categories,
    }
    
    return render(request, 'Admin/user_history.html', context)


@user_passes_test(is_admin , login_url='no_permission')
def Create_Group(request ):

    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request , f'Group {group.name} has been created successfully .')
            return redirect('Create_Group')  

    return render(request , 'Admin/create_group.html' , {'form':form})   


"""

@user_passes_test(is_admin , login_url='no_permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render( request , 'Admin/group_list.html', {'groups':groups} )

"""
@login_required
def update_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileCreate_Update_Form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')

    else:
        form = ProfileCreate_Update_Form(instance=profile)

    return render(request, 'Registrations/profile_form.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user  
    if user.groups.filter(name='Admin').exists():
        return redirect('Admin_dashboard')  
    elif user.groups.filter(name='Organizer').exists():
        return redirect('Organizer_Dashboard') 
    elif user.groups.filter(name='User').exists():
        return redirect('participant_dashboard')  

    return redirect('home')



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  
        print(user)

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()

        # Profile Information
        profile = getattr(user, 'profile', None)  
        print(profile)

        if profile:
            print(profile.bio)
            context['bio'] = profile.bio
            context['profile_picture'] = profile.profile_picture.url 
            context['phone'] = profile.phone
            context['address'] = profile.address
            context['date_of_birth'] = profile.date_of_birth

        # User Account Info
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login

        return context




class group_list( LoginRequiredMixin,UserPassesTestMixin, ListView):
    template_name = 'Admin/group_list.html'
    login_url = 'no_permission'
    model = Group

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.prefetch_related('permissions').all()
        return context



@user_passes_test(is_admin , login_url='no_permission')
def assigned_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignedRoleForm()
    if request.method == "POST":
        form = AssignedRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('Role')  # Ensure it matches the form field name
            user.groups.clear()  # Remove old roles
            user.groups.add(role)

            messages.success(request, f"{user.username} has been assigned to the '{role.name}' role")
            return redirect('Admin_dashboard')
    return render(request, 'Admin/assign_role.html', {"form": form, "user": user})

"""

@login_required
def participant_dashboard(request):
    user = request.user
    events = user.rsvped_events.all() 
    return render(request, 'Participants/participants_dashboard.html', {'events': events})

"""


class participant_dashboard(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'Participants/participants_dashboard.html'
    context_object_name = 'events'

    def get_queryset(self):
        return self.request.user.rsvped_events.all()



class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'Registrations/password_reset.html'
    success_url = reverse_lazy('log-in')
    html_email_template_name = 'Registrations/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'Registrations/password_reset.html'
    success_url = reverse_lazy('log-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)