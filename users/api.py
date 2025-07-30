from .models import User, Trainer_profile
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, TrainerProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    serializer_class = UserSerializer