from .models import Training_types, Training_sessions
from rest_framework import viewsets, permissions
from .serializers import TrainingTypeSerializer, TrainingSessionSerializer

class TrainingTypeViewSet(viewsets.ModelViewSet):
    queryset = Training_types.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TrainingTypeSerializer

class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = Training_sessions.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TrainingSessionSerializer
