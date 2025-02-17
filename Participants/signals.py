from django.db.models.signals import post_save , pre_save , pre_delete , post_delete ,m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


# @receiver(m2m_changed , sender = Task.employee.through)
# def Notify_employee_on_task_creation(sender , instance , action,**kwargs):        
#     if action=="post_add":
#         assigned_emails = [emp.email for emp in instance.employee.all()]
#         print(assigned_emails)
#         send_mail(
#             "Checkout your new task ",
#             f"You have been assigned to this task : {instance.title}",
#             "kashem.khondaker.official001@gmail.com",
#             assigned_emails,
#             fail_silently=False,   # for show error when main not send !
#         )



@receiver(post_save , sender = User)
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


@receiver(post_save , sender=User)
def assign_role(sender , instance , created , **kwargs):
    if created:
        user_group , created = Group.objects.get_or_create(name="User")
        instance.groups.add(user_group)
        instance.save()
