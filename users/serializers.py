# users/serializers.py
from rest_framework import serializers
from .models import CustomUser, Trainer_profile

# Este serializer es para la creación de usuarios (registro)
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

# Este serializer es para ver y editar el perfil de un usuario
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active']
        read_only_fields = ['id', 'username', 'email']
        
# Este serializer es para ver y editar el perfil de un entrenador
class TrainerProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Trainer_profile
        fields = ['id', 'user', 'specialty', 'bio']