from rest_framework import serializers
from .models import User, Trainer_profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'created_at')
        read_only_fields = ('created_at',)

class TrainerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer_profile
        fields = ('id', 'user', 'specialty', 'bio')
        read_only_fields = ('user',)
    
    