from django.db import models
from events.models import Event
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_image', blank=True, default='profile_images/default_img.jpg')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Participant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='participant_profile', null=True, default=None)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default_profile.jpg')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
