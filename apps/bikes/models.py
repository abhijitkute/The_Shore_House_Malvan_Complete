from django.db import models

class BikeCategory(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class RentalBike(models.Model):
    category = models.ForeignKey(BikeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="bikes/", blank=True, null=True)
    availability = models.BooleanField(default=True)
    def __str__(self): return self.name
