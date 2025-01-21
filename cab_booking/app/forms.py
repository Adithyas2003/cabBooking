from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'name', 'address', 'phone_number']

    start_date = forms.DateField()
    end_date = forms.DateField()
    name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15, required=False)


    