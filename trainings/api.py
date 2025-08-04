# trainings/api.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import F
from .models import TrainingType, TrainingSession
from .serializers import TrainingTypeSerializer, TrainingSessionSerializer, TrainingSessionCreateSerializer
from users.permissions import IsAdmin, IsTrainer, IsMember # Asumiendo que tienes estos permisos

# Vista para que los administradores gestionen los tipos de entrenamiento
class AdminTrainingTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainingType.objects.all()
    serializer_class = TrainingTypeSerializer
    permission_classes = [IsAdmin]

# Vista para que todos los usuarios vean los tipos de entrenamiento
class TrainingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrainingType.objects.all()
    serializer_class = TrainingTypeSerializer
    permission_classes = [permissions.AllowAny]

# Vista para que los administradores gestionen las sesiones de entrenamiento
class AdminTrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsAdmin]

# Vista para que los trainers y members vean sus sesiones de entrenamiento
class TrainingSessionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TrainingSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtra las sesiones para que solo el usuario logueado pueda verlas
        user = self.request.user
        if user.is_authenticated:
            # Si el usuario es un miembro, devuelve sus sesiones
            if user.role == 'member':
                return TrainingSession.objects.filter(user=user).order_by('date')
            # Si el usuario es un entrenador, devuelve sus sesiones
            elif user.role == 'trainer':
                return TrainingSession.objects.filter(trainer__user=user).order_by('date')
        return TrainingSession.objects.none()
    
# Vista para que los miembros gestionen sus sesiones de entrenamiento
class MemberTrainingSessionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsMember]

    def get_queryset(self):
        # Filtra las sesiones para que solo el miembro logueado pueda verlas
        return TrainingSession.objects.filter(user=self.request.user.customuser).order_by('date')

    @action(detail=False, methods=['post'], url_path='create-session')
    def create_session(self, request):
        serializer = TrainingSessionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        training_type_id = serializer.validated_data['training_type_id']
        training_type = TrainingType.objects.get(id=training_type_id)
        
        # Asigna el usuario y guarda la sesión
        TrainingSession.objects.create(
            user=request.user.customuser,
            training_type=training_type,
            date=serializer.validated_data['date'],
            duration_minutes=serializer.validated_data['duration_minutes'],
            notes=serializer.validated_data.get('notes', '')
        )
        
        return Response({'message': 'Training session created successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_session(self, request, pk=None):
        try:
            # 1. Obtener la sesión de entrenamiento específica
            training_session = self.get_object()
        except TrainingSession.DoesNotExist:
            return Response({'error': 'La sesión de entrenamiento no existe.'}, status=status.HTTP_404_NOT_FOUND)

        # 2. Verificar que el usuario que intenta cancelar sea el dueño de la sesión
        if training_session.user.id != request.user.customuser.id:
            return Response({'error': 'No tienes permiso para cancelar esta sesión.'}, status=status.HTTP_403_FORBIDDEN)

        # 3.1. No permitir cancelar sesiones que ya pasaron
        if training_session.date < timezone.now():
            return Response({'error': 'No se puede cancelar una sesión que ya ha pasado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 3.2 No permitir cancelar con menos de 24 horas de antelación
        if (training_session.date - timezone.now()).days < 1:
           return Response({'error': 'La cancelación debe hacerse con al menos 24 horas de antelación.'}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Eliminar la sesión
        training_session.delete()

        return Response({'message': 'La sesión de entrenamiento ha sido cancelada exitosamente.'}, status=status.HTTP_204_NO_CONTENT)

