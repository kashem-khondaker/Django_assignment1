from django.urls import path
from Participants.views import assigned_role, group_list ,activate_account ,admin_dashboard , Add_participants,update_Participants,delete_participant , User_Registrations , User_Log_in , User_Log_Out,Create_Group

urlpatterns = [
    path('add-participants/' , Add_participants , name="add_participant"),
    path('update/<int:id>/',update_Participants,name='update_Participants'),
    path('delete/<int:id>/',delete_participant,name='delete_participant'),
    path('sign-up/' , User_Registrations , name="sign-up"),
    path('log-in/' , User_Log_in , name="log-in"),
    path('log-out/' , User_Log_Out , name="log-out"),
    path('activate/<int:user_id>/<str:token>/', activate_account, name="activate_account"),
    path('admin/dashboard/' , admin_dashboard ,name="Admin_dashboard"),
    path('admin/create-group/' , Create_Group , name="Create_Group"),
    path('admin/group-list/' , group_list , name="group_list"),
    path('admin/assigned-role/<int:user_id>' , assigned_role , name="assigned_role"),
]
