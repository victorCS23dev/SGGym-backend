# memberships/api.py
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
from users.permissions import IsAdmin, IsMember
from .models import MembershipPlan, Membership
from .serializers import MembershipPlanSerializer, MembershipSerializer, MembershipPurchaseSerializer, AdminMembershipSerializer
from payments.models import Payment
from django.contrib.contenttypes.models import ContentType
import uuid

# Vista para los planes de membresía, solo se permite la lectura
class MembershipPlanViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = MembershipPlan.objects.filter(is_active=True)
    serializer_class = MembershipPlanSerializer
    permission_classes = [AllowAny]

# Vista para la gestión de planes de membresía por parte de un administrador
class AdminMembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAdmin]

# Vista para que el usuario gestione su propia membresía
class MembershipViewSet(viewsets.GenericViewSet):
    serializer_class = MembershipSerializer
    permission_classes = [IsMember]

    def get_queryset(self):
        # Un usuario solo puede ver su propia membresía
        return Membership.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Muestra la membresía actual del usuario
        queryset = self.get_queryset()
        if queryset.exists():
            instance = queryset.first()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({'detail': 'No membership found for this user.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='purchase')
    def purchase_membership(self, request):
        serializer = MembershipPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            plan_id = serializer.validated_data['plan_id']
            try:
                plan = MembershipPlan.objects.get(id=plan_id, is_active=True)
            except MembershipPlan.DoesNotExist:
                return Response({'error': 'Membership plan not found.'}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user

            # Lógica para extender la membresía
            try:
                # Si el usuario ya tiene una membresía, la extendemos
                membership = Membership.objects.get(user=user)
                
                # Calculamos la nueva fecha de finalización a partir de la fecha de finalización actual
                new_end_date = membership.end_date + timedelta(days=plan.duration_months * 30)
                
                # Actualizamos solo los campos necesarios
                membership.plan = plan
                membership.end_date = new_end_date
                membership.status = Membership.STATUS_ACTIVE
                membership.save()

                response_serializer = MembershipSerializer(membership)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            except Membership.DoesNotExist:
                # Si es una nueva membresía, la creamos desde cero
                new_start_date = timezone.now().date()
                new_end_date = new_start_date + timedelta(days=plan.duration_months * 30)
                
                membership = Membership.objects.create(
                    user=user,
                    plan=plan,
                    start_date=new_start_date,
                    end_date=new_end_date,
                    status=Membership.STATUS_ACTIVE
                )

                # 1. Simulación de pago
                content_type = ContentType.objects.get_for_model(Membership)
                transaction_id = str(uuid.uuid4())
                payment = Payment.objects.create(
                    user=user,
                    amount=plan.price,
                    status=Payment.STATUS_SUCCESS,
                    content_type=content_type,
                    object_id=membership.id,
                    transaction_id=transaction_id
                )

                response_serializer = MembershipSerializer(membership)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Vista para que un administrador gestione las membresías de los usuarios
class AdminMembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = AdminMembershipSerializer
    permission_classes = [IsAdmin]
