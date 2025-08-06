# users/serializers.py
from rest_framework import serializers
from .models import CustomUser, TrainerProfile

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name']

class SimpleTrainerProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = TrainerProfile
        fields = ['id', 'user', 'specialty']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Esta función sobrescribe el método 'create' para que la contraseña
        # se guarde de forma segura (hasheada) en la base de datos.
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'member') # Si no se especifica, el rol será 'member'
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'role', 'date_joined']

class AdminUserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class TrainerProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = TrainerProfile
        fields = ['id', 'user', 'specialty', 'bio']