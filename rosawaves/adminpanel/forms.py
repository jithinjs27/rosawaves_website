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
