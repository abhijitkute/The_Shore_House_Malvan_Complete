import json, io, base64
import qrcode
from decimal import Decimal
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Booking, BookingItem
from apps.coupons.models import Coupon
from apps.payments.models import Payment

User = get_user_model()

@csrf_exempt
def create_booking_api(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    try:
        user = User.objects.get(id=data.get("user_id"))
    except Exception:
        return JsonResponse({"error":"user not found"}, status=404)
    booking = Booking.objects.create(user=user, check_in=data.get("check_in"), check_out=data.get("check_out"), reference=f"BK{user.id}{Booking.objects.count()+1}")
    items = data.get("items", [])
    for it in items:
        app_label = it.get("app")
        object_id = it.get("object_id")
        price = Decimal(str(it.get("price","0.00")))
        quantity = int(it.get("quantity",1))
        if app_label == "rooms":
            model = __import__("apps.rooms.models", fromlist=["Room"]).Room
        elif app_label == "activities":
            model = __import__("apps.activities.models", fromlist=["WaterActivity"]).WaterActivity
        elif app_label == "bikes":
            model = __import__("apps.bikes.models", fromlist=["RentalBike"]).RentalBike
        else:
            continue
        ct = ContentType.objects.get_for_model(model)
        BookingItem.objects.create(booking=booking, content_type=ct, object_id=object_id, quantity=quantity, price=price)
    coupon_code = data.get("coupon_code")
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code__iexact=coupon_code)
            if coupon.is_valid():
                booking.coupon = coupon
                coupon.used_count += 1
                coupon.save()
        except Coupon.DoesNotExist:
            pass
    booking.calculate_totals()
    booking.save()
    method = data.get("payment_method","upi")
    payment = Payment.objects.create(booking=booking, amount=booking.final_amount, method=method, status=Payment.PENDING)
    upi_payload = None
    if method in ("upi","qr"):
        upi_payload = f"upi://pay?pa={{VPA}}&pn=The+Shore+House+Malvan&tn={booking.reference}&am={booking.final_amount}&cu=INR"
        payment.qr_payload = upi_payload
        payment.save()
    try:
        subject = f"Booking Received: {booking.reference}"
        message = f"Your booking {booking.reference} of amount {booking.final_amount} is created. Complete payment."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email, settings.MANAGER_EMAIL], fail_silently=True)
    except Exception:
        pass
    qr_base64 = None
    if upi_payload:
        img = qrcode.make(upi_payload)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode()
    return JsonResponse({"booking_id": booking.id, "final_amount": str(booking.final_amount), "payment_id": payment.id, "qr_payload": upi_payload, "qr_base64": qr_base64})
