from django import forms
from rosawaves_app.models import BikeRental # make sure these are imported

class ExtendBookingForm(forms.ModelForm):
    class Meta:
        model = BikeRental
        fields = ['dropoff_date', 'bike_model']
        widgets = {
            'dropoff_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bike_model': forms.Select(attrs={'class': 'form-select'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = BikeRental
        fields = ['full_name', 'email', 'phone', 'bike_model', 'rental_days', 'pickup_date', 'dropoff_date', 'license_number']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'dropoff_date': forms.DateInput(attrs={'type': 'date'}),
        }

