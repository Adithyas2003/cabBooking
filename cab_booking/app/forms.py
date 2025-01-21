from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'name', 'address', 'phone_number','total_amount','status','confirmation_code']

    start_date = forms.DateField()
    end_date = forms.DateField()
    name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15, required=False)
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    status=forms.CharField(max_length=25)
    confirmation_code=forms.CharField(max_length=6)
