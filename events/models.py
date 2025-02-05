from django.db import models
from categories.models import Categories

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Categories , on_delete=models.CASCADE , related_name='event')

    def __str__(self):
        return self.title
