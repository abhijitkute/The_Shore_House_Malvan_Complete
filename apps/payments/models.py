from django.db import models
class Payment(models.Model):
    UPI='upi'
    CARD='card'
    QR='qr'
    PAYMENT_METHODS=[(UPI,'UPI'),(CARD,'Card'),(QR,'QR')]
    PENDING='pending'; SUCCESS='success'; FAILED='failed'
    STATUS=[(PENDING,'Pending'),(SUCCESS,'Success'),(FAILED,'Failed')]
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS, default=PENDING)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_payload = models.TextField(blank=True, null=True)
    def __str__(self): return f"Payment {self.id} for Booking {self.booking.id}"
