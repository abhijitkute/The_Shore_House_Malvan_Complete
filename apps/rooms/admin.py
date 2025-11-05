from django.contrib import admin
from .models import Room, RoomCategory
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name','category','price_per_night','is_active')
@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
