from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BikeModel,accessories

@admin.register(BikeModel)
class BikeModelAdmin(admin.ModelAdmin):
    list_display = ['name','Vehicle_number']
    search_fields = ['Vehicle_number']

@admin.register(accessories)
class BikeModelAdmin(admin.ModelAdmin):
    list_display = ['Helmet_Id','Helmet_name']
    search_fields = ['Helmet_Id']
