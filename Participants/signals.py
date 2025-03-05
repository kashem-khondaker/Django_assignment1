from django.db.models.signals import post_save , pre_save , pre_delete , post_delete ,m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from events.models import Event
from .models import Participant
from Participants.models import CustomUser

@receiver(m2m_changed, sender=Event.rsvped_users.through)
def send_rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = instance.rsvped_users.get(id=user_id)
            send_mail(
                "RSVP Confirmation",
                f"Hello {user.first_name},\n\nYou have successfully RSVP’d for {instance.title} on {instance.date} at {instance.time}.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )



@receiver(m2m_changed, sender=Participant.events.through)
def send_rsvp_email(sender, instance, action, **kwargs):
    if action == "post_add":  
        for event in instance.events.all():
            send_mail(
                "RSVP Confirmation",
                f"Hello {instance.name},\n\nYou have successfully RSVP’d for {event.title} on {event.date} at {event.time}.",
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )



@receiver(post_save , sender=settings.AUTH_USER_MODEL )
def send_activation_email(sender , instance , created , **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/participants/activate/{instance.id}/{token}/"

        subject = "Activate your Account "
        message = f' Hi , {instance.username}\n\n Please activate your account by thin link : \n\n {activation_url}\n\n Thanks From Task Team'

        recipient_list = [instance.email]
        try :
            send_mail(subject , message,settings.EMAIL_HOST_USER,recipient_list)
        except Exception as E:
            print(f"Failed to send email to {instance.email} : {str(E)}")


@receiver(post_save , sender=settings.AUTH_USER_MODEL )
def assign_role(sender , instance , created , **kwargs):
    if created:
        user_group , created = Group.objects.get_or_create(name="User")
        instance.groups.add(user_group)
        instance.save()
