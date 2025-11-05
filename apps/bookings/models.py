from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from apps.coupons.models import Coupon

User = settings.AUTH_USER_MODEL

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    reference = models.CharField(max_length=64, blank=True, null=True)

    def calculate_totals(self):
        items = self.items.all()
        total = sum([it.line_total for it in items]) or Decimal('0.00')
        self.total_amount = total
        discount = Decimal('0.00')
        if self.coupon and self.coupon.is_valid():
            if self.coupon.coupon_type == Coupon.PERCENT:
                discount = (self.total_amount * (self.coupon.value / Decimal('100.0')))
            else:
                discount = self.coupon.value
        self.discount_amount = min(discount, self.total_amount)
        self.final_amount = (self.total_amount - self.discount_amount)
        return self.final_amount

class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, related_name='items', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)

    @property
    def line_total(self):
        return self.price * self.quantity
