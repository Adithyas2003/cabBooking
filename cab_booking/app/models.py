from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cab(models.Model):
    number_plate = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=100)
    available = models.IntegerField()
    def __str__(self):
        return f'{self.model} ({self.number_plate})'