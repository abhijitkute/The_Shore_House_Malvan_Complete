from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    PERCENT='percent'
    FIXED='fixed'
    COUPON_TYPE_CHOICES=[(PERCENT,'Percentage'),(FIXED,'Fixed amount')]
    code = models.CharField(max_length=50, unique=True)
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPE_CHOICES, default=PERCENT)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        now = timezone.now()
        if not self.active:
            return False
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_to and now > self.valid_to:
            return False
        if self.max_uses is not None and self.used_count >= self.max_uses:
            return False
        return True

    def __str__(self):
        return self.code
