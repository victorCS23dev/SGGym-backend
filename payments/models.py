# payments/models.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser


# Create your models here.
class Payment(models.Model):
    STATUS_SUCCESS = 'success'
    STATUS_PENDING = 'pending'
    STATUS_FAILED = 'failed'

    PAYMENT_STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Success'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_FAILED, 'Failed'),
    ]

    PAYMENT_METHOD_CARD = 'credit_card'
    PAYMENT_METHOD_PAYPAL = 'paypal'
    PAYMENT_METHOD_BANK_TRANSFER = 'bank_transfer'

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_CARD, 'Credit Card'),
        (PAYMENT_METHOD_PAYPAL, 'PayPal'),
        (PAYMENT_METHOD_BANK_TRANSFER, 'Bank Transfer'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default=STATUS_PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    def __str__(self):
        return f'Payment {self.transaction_id} - {self.user.username} - {self.amount} ({self.status})'