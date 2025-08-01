# payments/api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
import uuid 

from .models import Payment
from .serializers import PaymentSubmissionSerializer, PaymentSerializer

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PaymentSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            # Obtiene los datos validados del serializer
            amount = serializer.validated_data['amount']
            payment_method = serializer.validated_data['payment_method']
            description = serializer.validated_data.get('description', '')
            content_type_model = serializer.validated_data['content_type_model']
            object_id = serializer.validated_data['object_id']

            # Verifica si el objeto a pagar existe
            try:
                content_type = ContentType.objects.get(model=content_type_model)
                content_object = content_type.get_object_for_this_type(pk=object_id)
            except (ContentType.DoesNotExist, content_type.model_class().DoesNotExist):
                return Response({'error': 'El objeto a pagar no existe.'}, status=status.HTTP_400_BAD_REQUEST)

            # --- Aquí es donde se genera o se recibe la información clave ---
            # En un entorno real, aquí se llamaría a una API de pagos externa.
            # Por ahora, simulamos un ID de transacción único.
            transaction_id = str(uuid.uuid4())
            
            # Por ahora, simulamos un pago exitoso
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                payment_method=payment_method,
                status=Payment.STATUS_SUCCESS,
                description=description,
                transaction_id=transaction_id,
                content_type=content_type,
                object_id=object_id,
            )
            
            response_serializer = PaymentSerializer(payment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)