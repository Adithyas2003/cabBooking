from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    vehicle = forms.CharField(max_length=100)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
