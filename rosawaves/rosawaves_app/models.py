# rental/models.py
from django.db import models
from adminpanel.models import BikeModel  # Import from the other app

class BikeRental(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,default="none")
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    alternate_ph=models.CharField(max_length=15,default="1")
    emergency_ph=models.CharField(max_length=15,default="1")
    upid=models.CharField(max_length=50,default="none")
    bike_model = models.CharField(max_length=50)
    bike_number=models.CharField(max_length=50,default="none")
    rental_days = models.CharField(max_length=50)
    pickup_date = models.DateTimeField()
    dropoff_date = models.DateTimeField()
    rider_pic = models.ImageField(upload_to='riders/')
    license_number = models.CharField(max_length=50)
    aadhar_upload = models.FileField(upload_to='aadhar_docs/')
    passport_upload = models.FileField(upload_to='passport_docs/', blank=True, null=True)
    hotel_upload = models.FileField(upload_to='hotel_docs/', blank=True, null=True)
    status=models.CharField(max_length=50,default="pending")
    deposit_amount=models.PositiveIntegerField(default=0)
    total_bill_amount=models.PositiveIntegerField(default=0)
    advance_amount=models.PositiveIntegerField(default=0)
    remarks=models.CharField(max_length=50,default="none")
    Name_of_staff=models.CharField(max_length=50,default="none")
    helmet_1=models.CharField(max_length=50,default="none")
    helmet_2=models.CharField(max_length=50,default="none")
    payment_status=models.CharField(max_length=50,default="none")
    razorpay_payment_id=models.CharField(max_length=50,default="none")


