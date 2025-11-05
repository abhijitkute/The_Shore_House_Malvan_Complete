from django.shortcuts import render, redirect
from .models import Coupon

def coupon_apply(request):
    message = None
    if request.method == "POST":
        code = request.POST.get("code","").strip()
        try:
            c = Coupon.objects.get(code__iexact=code)
            if c.is_valid():
                message = "Coupon applied!"
            else:
                message = "Coupon is not valid."
        except Coupon.DoesNotExist:
            message = "Coupon not found."
    return render(request, "coupons/coupon_apply.html", {"message": message})
