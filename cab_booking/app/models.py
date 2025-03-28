from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cab(models.Model):
    pid=models.TextField()
    vehicle_type = models.CharField(max_length=100) 
    number_plate = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=100)
    seats = models.IntegerField(null=True, blank=True)  

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
    confirmation_code = models.CharField(max_length=6, unique=True) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    name = models.CharField(max_length=255)  
    address = models.TextField() 
    location = models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[("PENDING", "Pending"), ("PAID", "Paid")], default="PENDING")
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"Booking for {self.vehicle.vehicle_type} by {self.user.username}"

class Vehicle(models.Model):
   
    vehicle_type = models.CharField(max_length=100) 
    seating_capacity = models.IntegerField()  
    rate_per_day = models.DecimalField(max_digits=8, decimal_places=2)  
    allowed_km_per_day = models.IntegerField() 
    cost_per_extra_km = models.DecimalField(max_digits=8, decimal_places=2)  
    
    def __str__(self):
        return self.vehicle_type
    
class Address(models.Model):
    name=models.CharField(max_length=255)
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=20)

class Contact(models.Model):
    full_name=models.CharField(max_length=255)
    email_address=models.EmailField(max_length=255)
    message=models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)
def __str__(self):
    return self.full_name


