# payments/api.py
from rest_framework import viewsets
from rest_framework import serializers
from users.permissions import IsAdmin, IsMember
from .models import Payment
from .serializers import PaymentSerializer


# Vista para manejar los pagos
class PaymentView(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    

# Vista para ver los pagos realizados por un usuario
class UserPaymentsView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsMember]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-timestamp')

