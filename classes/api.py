# classes/views.py
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db.models import F

from .models import ClassType, GymClass, ClassReservation, ClassMembershipAccess
from .serializers import (
    ClassTypeSerializer, GymClassSerializer,
    ClassReservationSerializer, ClassReservationCreateSerializer, ClassMembershipAccessSerializer
)
from users.permissions import IsAdmin, IsTrainer, IsMember
from memberships.models import Membership

# Vista para que los administradores gestionen los tipos de clases
class AdminClassTypeViewSet(viewsets.ModelViewSet):
    queryset = ClassType.objects.all()
    serializer_class = ClassTypeSerializer
    permission_classes = [IsAdmin]

# Vista para que los usuarios vean los tipos de clases
class ClassTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClassType.objects.all()
    serializer_class = ClassTypeSerializer
    permission_classes = [AllowAny]

# Vista para que los administradores gestionen las clases
class AdminGymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.all()
    serializer_class = GymClassSerializer
    permission_classes = [IsAdmin]

# Vista para que los usuarios vean las clases
class GymClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GymClass.objects.filter(date__gte=timezone.now()).order_by('date')
    serializer_class = GymClassSerializer
    permission_classes = [AllowAny]

# Vista para que los usuarios reserven clases
class UserGymClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GymClass.objects.filter(date__gte=timezone.now()).order_by('date')
    serializer_class = GymClassSerializer
    permission_classes = [IsAuthenticated]
    
    # Acción para que un usuario reserve una clase
    @action(detail=False, methods=['post'], url_path='reserve')
    def reserve_class(self, request):
        # 1. Validar los datos de entrada con el serializer
        serializer = ClassReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        gym_class = serializer.validated_data['gym_class']
        
        user = request.user

        # 2. Verificar si el usuario tiene membresía activa
        try:
            membership = Membership.objects.get(user=user, status=Membership.STATUS_ACTIVE)
            if membership.end_date < timezone.now().date():
                return Response({'error': 'Your membership has expired.'}, status=status.HTTP_403_FORBIDDEN)
        except Membership.DoesNotExist:
            return Response({'error': 'You need an active membership to reserve a class.'}, status=status.HTTP_403_FORBIDDEN)
        
        # 3. Verificar el acceso del plan de membresía a este tipo de clase
        access_granted = ClassMembershipAccess.objects.filter(
            membership_plan=membership.plan,
            class_type=gym_class.class_type
        ).exists()
        
        if not access_granted:
            return Response({'error': 'Your membership plan does not grant access to this class.'}, status=status.HTTP_403_FORBIDDEN)

        # 4. Verificar si hay espacio en la clase
        current_reservations = ClassReservation.objects.filter(gym_class=gym_class).count()
        if current_reservations >= gym_class.max_participants:
            return Response({'error': 'Class is full.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 5. Verificar si el usuario ya reservó esta clase
        if ClassReservation.objects.filter(user=user, gym_class=gym_class).exists():
            return Response({'error': 'You have already reserved a spot in this class.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 6. Crear la reserva
        reservation = ClassReservation.objects.create(user=user, gym_class=gym_class)
        serializer = ClassReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# Vista para que los administradores gestionen las reservas de clases
class AdminClassMembershipAccessViewSet(viewsets.ModelViewSet):
    queryset = ClassMembershipAccess.objects.all()
    serializer_class = ClassMembershipAccessSerializer
    permission_classes = [IsAdmin] # Solo los administradores pueden gestionar estas reglas