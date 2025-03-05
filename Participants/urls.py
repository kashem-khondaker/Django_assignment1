from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView , PasswordResetDoneView , PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView
from Participants.views import participant_dashboard, assigned_role, group_list ,activate_account ,admin_dashboard , Add_participants,update_Participants,delete_participant , User_Registrations , User_Log_in , User_Log_Out,Create_Group,all_event , User_history,no_permission , update_profile  , ProfileView , dashboard , CustomPasswordResetView , CustomPasswordResetConfirmView



urlpatterns = [
    # path('p-dashboard/' , participant_dashboard , name="participant_dashboard"),
    path('p-dashboard/' , participant_dashboard.as_view() , name="participant_dashboard"),
    path('add-participants/' , Add_participants , name="add_participant"),
    path('update/<int:id>/',update_Participants,name='update_Participants'),
    path('delete/<int:id>/',delete_participant,name='delete_participant'),
    path('sign-up/' , User_Registrations.as_view() , name="sign-up"),
    # path('log-in/' , User_Log_in , name="log-in"),
    path('log-in/' , User_Log_in.as_view() , name="log-in"),
    # path('log-out/' , User_Log_Out , name="log-out"),
    path('log-out/' , User_Log_Out.as_view() , name="log-out"),
    path('activate/<int:user_id>/<str:token>/', activate_account, name="activate_account"),
    path('admin/dashboard/' , admin_dashboard ,name="Admin_dashboard"),
    path('admin/create-group/' , Create_Group , name="Create_Group"),
    # path('admin/group-list/' , group_list , name="group_list"),
    path('admin/group-list/' , group_list.as_view() , name="group_list"),
    path('admin/assigned-role/<int:user_id>' , assigned_role , name="assigned_role"),
    path('admin/event/all/',all_event , name="all_event"),
    path('admin/user/history/' , User_history , name="user_history"),
    path('no_permission/',no_permission , name="no_permission"),
    path('profile/', ProfileView.as_view() , name='profile'),
    path('update-profile/' , update_profile , name='update_profile'),
    path('dashboard/' , dashboard , name="dashboard"),
    path('password-change/', PasswordChangeView.as_view(template_name='Registrations/password_change.html') , name="password_change"),
    path('password-change/done/' , PasswordChangeDoneView.as_view(template_name='Registrations/password_change_done.html') , name="password_change_done"),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
