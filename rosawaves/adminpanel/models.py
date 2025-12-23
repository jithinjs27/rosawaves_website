from django.db import models
from django.utils import timezone
class BikeModel(models.Model):
    name = models.CharField(max_length=100)
    Vehicle_number= models.CharField(max_length=20,unique=True)
    mileage = models.CharField(max_length=20, blank=True)
    rent_per_day = models.PositiveIntegerField()
    Onwer_name=models.CharField(max_length=20, blank=True)
    Status=models.CharField(max_length=20, default="Free")
    bike_image=models.FileField(upload_to='bike_pics/', blank=True, null=True)
    available_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
class offers(models.Model):
    offer_image=models.FileField(upload_to='offers_dir/', blank=True, null=True)
    description=models.CharField(max_length=150, blank=True)

class accessories(models.Model):
    Helmet_Id=models.CharField(max_length=150, blank=True)
    Helmet_name=models.CharField(max_length=150, blank=True)
    status=models.CharField(max_length=20, default="Available")
    helmet_image=models.FileField(upload_to='helmet_pics/', blank=True, null=True)
    def __str__(self):
        return f"{self.Helmet_Id} - {self.Helmet_name}"
