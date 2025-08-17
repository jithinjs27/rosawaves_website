from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BikeModel

@admin.register(BikeModel)
class BikeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'mileage', 'rent_per_day']
    search_fields = ['name']
