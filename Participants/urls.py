from django.urls import path
from Participants.views import Participants  , Add_participants,update_Participants,delete_participant , User_Registrations , User_Log_in , User_Log_Out

urlpatterns = [
    path('', Participants, name='participant_list'), 
    path('add-participants/' , Add_participants , name="add_participant"),
    path('update/<int:id>/',update_Participants,name='update_Participants'),
    path('delete/<int:id>/',delete_participant,name='delete_participant'),
    path('sign-up/' , User_Registrations , name="sign-up"),
    path('log-in/' , User_Log_in , name="log-in"),
    path('log-out/' , User_Log_Out , name="log-out"),
]
