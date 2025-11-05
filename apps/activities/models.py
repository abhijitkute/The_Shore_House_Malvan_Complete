from django.db import models

class ActivityCategory(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class WaterActivity(models.Model):
    category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    capacity = models.PositiveIntegerField(default=10)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField(null=True, blank=True)
    image = models.ImageField(upload_to="activities/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.title
