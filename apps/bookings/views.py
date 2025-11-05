from django.shortcuts import render, get_object_or_404
from .models import Booking

def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, "booking/booking_list.html", {"bookings": bookings})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, "booking/booking_detail.html", {"booking": booking})
