from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'name', 'address', 'phone_number', 'total_amount', 'status']
        # Add the necessary fields from your model

