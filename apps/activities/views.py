from django.shortcuts import render, get_object_or_404
from .models import WaterActivity

def activity_list(request):
    activities = WaterActivity.objects.filter(is_active=True)
    return render(request, "activities/activity_list.html", {"activities": activities})

def activity_detail(request, pk):
    activity = get_object_or_404(WaterActivity, pk=pk)
    return render(request, "activities/activity_detail.html", {"activity": activity})
