# payments/serializers.py
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    related_object = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'amount', 'payment_method', 'status',
            'timestamp', 'description', 'transaction_id',
            'related_object'
        ]
        read_only_fields = ['id', 'user', 'status', 'timestamp', 'transaction_id', 'related_object']

    def get_related_object(self, obj):
        if obj.content_object:
            return {
                'id': obj.object_id,
                'model_name': obj.content_type.model,
                'representation': str(obj.content_object)
            }
        
        # Lógica de depuración si el objeto no se encuentra
        try:
            # Intentamos obtener el ContentType
            content_type_obj = ContentType.objects.get(id=obj.content_type_id)
            return {
                'error': f'El objeto {content_type_obj.model} con ID {obj.object_id} no existe en la base de datos.'
            }
        except ContentType.DoesNotExist:
            return {
                'error': f'El ContentType con ID {obj.content_type_id} no existe.'
            }
        except Exception as e:
            return {
                'error': f'Error desconocido al obtener el objeto relacionado: {str(e)}'
            }


class PaymentSubmissionSerializer(serializers.Serializer):
    # Serializer de solo escritura para recibir los datos del pago desde el cliente
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)
    content_type_model = serializers.CharField()
    object_id = serializers.IntegerField()

# Serializer para ver los pagos realizados por un usuario
class UserPaymentsSerializer(serializers.Serializer):
    related_object = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'payment_method', 'status',
            'timestamp', 'description', 'transaction_id',
            'related_object' 
            ]
        read_only_fields = [
            'id', 'amount', 'payment_method', 'status',
            'timestamp', 'description', 'transaction_id',
            'related_object'
            ]

    def get_related_object(self, obj):
        if obj.content_object:
            model_name = obj.content_type.model
            
            if model_name == 'membership':
                return {
                    'id': obj.object_id,
                    'model_name': model_name,
                }
            
            if model_name == 'class':
                return {
                    'id': obj.object_id,
                    'model_name': model_name,
                }
            
            return {
                'id': obj.object_id,
                'model_name': model_name,
                'representation': str(obj.content_object)
            }
        return None
