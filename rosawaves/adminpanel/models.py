from django.db import models

class BikeModel(models.Model):
    name = models.CharField(max_length=100)
    Vehicle_number= models.CharField(max_length=20, blank=True)
    mileage = models.CharField(max_length=20, blank=True)
    rent_per_day = models.PositiveIntegerField()
    Onwer_name=models.CharField(max_length=20, blank=True)
    Status=models.CharField(max_length=20, default="Free")

    def __str__(self):
        return self.name
class offers(models.Model):
    offer_image=models.FileField(upload_to='offers_dir/', blank=True, null=True)
    description=models.CharField(max_length=150, blank=True)
