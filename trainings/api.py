from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import F
from .models import TrainingType, TrainingSession, TrainingRequest
from .serializers import (
    TrainingTypeSerializer, TrainingSessionSerializer, 
    TrainingRequestSerializer
)
from users.models import TrainerProfile
from users.permissions import IsAdmin, IsMember, IsTrainer
from django.utils import timezone
from datetime import timedelta

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
        user = self.request.user
        if user.is_authenticated:
            # Si el usuario es un miembro, devuelve sus sesiones
            if user.role == 'member':
                return TrainingSession.objects.filter(user=user).order_by('date')
            # Si el usuario es un entrenador, devuelve sus sesiones
            elif user.role == 'trainer':
                # Asegura que el usuario tiene un TrainerProfile antes de filtrar
                try:
                    trainer_profile = user.trainerprofile
                    return TrainingSession.objects.filter(trainer=trainer_profile).order_by('date')
                except TrainerProfile.DoesNotExist:
                    return TrainingSession.objects.none()
        return TrainingSession.objects.none()
    
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_session(self, request, pk=None):
        try:
            training_session = self.get_object()
        except TrainingSession.DoesNotExist:
            return Response({'error': 'La sesión de entrenamiento no existe.'}, status=status.HTTP_404_NOT_FOUND)

        if training_session.user.id != request.user.id:
            return Response({'error': 'No tienes permiso para cancelar esta sesión.'}, status=status.HTTP_403_FORBIDDEN)

        if training_session.date < timezone.now():
            return Response({'error': 'No se puede cancelar una sesión que ya ha pasado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if (training_session.date - timezone.now()).total_seconds() < 24 * 3600:
            return Response({'error': 'La cancelación debe hacerse con al menos 24 horas de antelación.'}, status=status.HTTP_400_BAD_REQUEST)

        training_session.delete()

        return Response({'message': 'La sesión de entrenamiento ha sido cancelada exitosamente.'}, status=status.HTTP_204_NO_CONTENT)


# Nueva vista para manejar las solicitudes de entrenamiento
class TrainingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingRequestSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'accept', 'reject']:
            self.permission_classes = [IsTrainer | IsAdmin]
        elif self.action == 'create':
            self.permission_classes = [IsMember]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'trainer':
            try:
                trainer_profile = user.trainerprofile
                return TrainingRequest.objects.filter(trainer=trainer_profile).order_by('-created_at')
            except TrainerProfile.DoesNotExist:
                return TrainingRequest.objects.none()
        elif user.role == 'member':
            return TrainingRequest.objects.filter(member=user).order_by('-created_at')
        return TrainingRequest.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Asigna el miembro que crea la solicitud
        serializer.save(member=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        training_request = self.get_object()
        
        if training_request.status != TrainingRequest.STATUS_PENDING:
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)

        # Si todo está bien, crea la sesión de entrenamiento
        TrainingSession.objects.create(
            user=training_request.member,
            trainer=training_request.trainer,
            training_type=training_request.training_type,
            date=training_request.requested_date,
            duration_minutes=training_request.duration_minutes,
            notes=f'Solicitud aceptada de: {training_request.notes}'
        )

        training_request.status = TrainingRequest.STATUS_ACCEPTED
        training_request.save()

        return Response({'message': 'Solicitud aceptada y sesión creada.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        training_request = self.get_object()

        if training_request.status != TrainingRequest.STATUS_PENDING:
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        training_request.status = TrainingRequest.STATUS_REJECTED
        training_request.save()

        return Response({'message': 'Solicitud rechazada.'}, status=status.HTTP_200_OK)