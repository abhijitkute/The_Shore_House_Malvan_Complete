from django.shortcuts import render, get_object_or_404
from .models import Room

def room_list(request):
    rooms = Room.objects.filter(is_active=True)
    return render(request, "rooms/room_list.html", {"rooms": rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, "rooms/room_detail.html", {"room": room})
