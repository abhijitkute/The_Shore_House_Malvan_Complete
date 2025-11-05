from django.shortcuts import render, get_object_or_404
from .models import Payment

def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, "payments/payment_page.html", {"payment": payment})
