# memberships/models.py
from django.db import models
from django.utils import timezone
from users.models import CustomUser

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_months = models.PositiveIntegerField(help_text="Duración del plan en meses")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.price} USD'

class Membership(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_EXPIRED = 'expired'
    STATUS_CANCELLED = 'cancelled'

    MEMBERSHIP_STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='membership')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

    def __str__(self):
        return f'{self.user.username} - {self.plan.name} ({self.status})'

    def is_active(self):
        # Método para verificar si la membresía está activa
        return self.status == self.STATUS_ACTIVE and self.end_date >= timezone.now().date()