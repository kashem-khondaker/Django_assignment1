from django.urls import path
from Participants.views import Participants  , Add_participants

urlpatterns = [
    path('', Participants, name='participant_list'), 
    path('add-participants/' , Add_participants , name="add_participant")
]
