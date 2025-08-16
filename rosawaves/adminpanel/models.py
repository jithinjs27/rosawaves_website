from django.db import models

class BikeModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mileage = models.CharField(max_length=20, blank=True)
    rent_per_day = models.PositiveIntegerField()
    deposit_amount=models.PositiveIntegerField()

    def __str__(self):
        return self.name
