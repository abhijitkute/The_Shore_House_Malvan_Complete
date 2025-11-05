from django.db import models

class RoomCategory(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="room_categories/", blank=True, null=True)
    def __str__(self): return self.name

class Room(models.Model):
    category = models.ForeignKey(RoomCategory, on_delete=models.SET_NULL, null=True, related_name="rooms")
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    max_guests = models.PositiveIntegerField(default=2)
    beds = models.PositiveIntegerField(default=1)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="rooms/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name
