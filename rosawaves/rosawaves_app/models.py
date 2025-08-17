# rental/models.py
from django.db import models
from adminpanel.models import BikeModel  # Import from the other app

class BikeRental(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    bike_model = models.CharField(max_length=50)
    rental_days = models.PositiveIntegerField()
    pickup_date = models.DateField()
    dropoff_date = models.DateField()
    rider_pic = models.ImageField(upload_to='riders/')
    license_number = models.CharField(max_length=50)
    aadhar_upload = models.FileField(upload_to='aadhar_docs/')
    status=models.CharField(max_length=50,default="pending")
    deposit_amount=models.PositiveIntegerField(default=0)
    total_bill_amount=models.PositiveIntegerField(default=0)
    advance_amount=models.PositiveIntegerField(default=0)
    remarks=models.PositiveIntegerField(default=0)

