from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import BikeRental

@admin.register(BikeRental)
class BikeRentalAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'bike_model', 'pickup_date', 'dropoff_date']
    search_fields = ['full_name', 'bike_model__name', 'license_number']
    list_filter = ['pickup_date', 'bike_model']

