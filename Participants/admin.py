from django.contrib import admin
from categories.models import Categories
from events.models import Event
from Participants.models import Participant

# Register your models here.

admin.site.register(Categories)
admin.site.register(Event)
admin.site.register(Participant)