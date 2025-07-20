from django import forms
from .models import BikeRental

class BikeRentalForm(forms.ModelForm):
    class Meta:
        model = BikeRental
        fields = '__all__'
