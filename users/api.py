# users/api.py
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth import get_user_model

# Importa tu modelo personalizado
from .models import TrainerProfile

# Importa tus serializers
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer, 
    TrainerProfileSerializer
)

# Importa tus permisos personalizados
from .permissions import IsAdmin, IsTrainer, IsMember

# La mejor práctica es usar get_user_model() para referirte a tu modelo de usuario
CustomUser = get_user_model()

# --- Vistas para APIs ---

# Vista para el registro de nuevos usuarios (accesible para cualquiera)
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

# ViewSet para que un usuario vea y edite su propio perfil
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Asegura que cada usuario solo pueda ver su propio perfil
        return CustomUser.objects.filter(pk=self.request.user.pk)

# ViewSet para que los administradores gestionen todos los usuarios
class AdminUserManagementViewSet(viewsets.ModelViewSet):
    # Aquí nos referimos al queryset de CustomUser directamente
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdmin] # Usamos el permiso que creaste

# ViewSet para que los trainers vean y editen su perfil de entrenador
class TrainerProfileViewSet(viewsets.ModelViewSet):
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer
    permission_classes = [IsTrainer] # Usamos el permiso que creaste

    def perform_create(self, serializer):
        # Lógica para asegurar que solo los entrenadores creen su perfil
        if not self.request.user.role == CustomUser.ROLE_TRAINER:
            return Response({"error": "Solo los entrenadores pueden crear su perfil."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Lógica para que cada entrenador vea solo su propio perfil
        if self.request.user.role == CustomUser.ROLE_TRAINER:
            return TrainerProfile.objects.filter(user=self.request.user)
        # Si el usuario no es un entrenador (pero está autenticado), no verá nada
        return TrainerProfile.objects.none()