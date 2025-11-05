from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def reviews(request):
    return render(request, 'reviews.html')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("rooms/", include("apps.rooms.urls")),
    path("activities/", include("apps.activities.urls")),
    path("bikes/", include("apps.bikes.urls")),
    path("bookings/", include("apps.bookings.urls")),
    path("payments/", include("apps.payments.urls")),
    path("coupons/", include("apps.coupons.urls")),
    path("api/bookings/create/", include("apps.bookings.api_urls")),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('reviews/', reviews, name='reviews'),
]
