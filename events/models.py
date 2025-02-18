from django.db import models
from categories.models import Categories
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='event')
    image = models.ImageField(upload_to='event_images/', default='event_images/default.jpg')

    # RSVP System
    rsvped_users = models.ManyToManyField(User, related_name='rsvped_events', blank=True)

    def clean(self):
        super().clean()
        if self.date < date.today():
            raise ValidationError({'date': 'Date cannot be in the past!'})

    def save(self, *args, **kwargs):
        """Ensure validation runs before saving."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
