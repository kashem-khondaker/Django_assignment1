from django.apps import AppConfig


class ParticipantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Participants'

    def ready(self):
        import Participants.signals