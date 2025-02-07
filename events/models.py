from django.db import models
from categories.models import Categories
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Categories , on_delete=models.CASCADE , related_name='event')

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
