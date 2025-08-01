# payments/serializers.py
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'amount', 'payment_method', 'status',
            'timestamp', 'description', 'transaction_id',
            'content_type', 'object_id'
        ]
        read_only_fields = ['id', 'user', 'status', 'timestamp', 'transaction_id']

class PaymentSubmissionSerializer(serializers.Serializer):
    # Serializer de solo escritura para recibir los datos del pago desde el cliente
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)
    content_type_model = serializers.CharField()
    object_id = serializers.IntegerField()