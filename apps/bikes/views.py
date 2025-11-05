from django.shortcuts import render, get_object_or_404
from .models import RentalBike

def bike_list(request):
    bikes = RentalBike.objects.filter(availability=True)
    return render(request, "bikes/bike_list.html", {"bikes": bikes})

def bike_detail(request, pk):
    bike = get_object_or_404(RentalBike, pk=pk)
    return render(request, "bikes/bike_detail.html", {"bike": bike})
