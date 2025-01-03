from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cab(models.Model):
    
    number_plate = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=100)
    available = models.IntegerField()
    price=models.IntegerField()
    img = models.FileField()

    def __str__(self):
        return f'{self.model} ({self.number_plate})'
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Cab, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    confirmation_code = models.CharField(max_length=10, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Booking for {self.vehicle.vehicle_type} by {self.user.username}"

