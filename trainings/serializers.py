from rest_framework import serializers
from .models import TrainingType, TrainingSession, TrainingRequest
from users.serializers import SimpleUserSerializer, SimpleTrainerProfileSerializer

class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = ['id', 'name', 'description']

class TrainingSessionSerializer(serializers.ModelSerializer):
    training_type = TrainingTypeSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)
    trainer = SimpleTrainerProfileSerializer(read_only=True)

    class Meta:
        model = TrainingSession
        fields = [
            'id', 'user', 'trainer', 'training_type', 
            'date', 'duration_minutes', 'notes'
        ]

# Serializer para que los miembros soliciten una sesión de entrenamiento
class TrainingRequestSerializer(serializers.ModelSerializer):
    member = SimpleUserSerializer(read_only=True)
    trainer_id = serializers.IntegerField(write_only=True)
    training_type_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = TrainingRequest
        fields = ['id', 'member', 'trainer_id', 'training_type_id', 'requested_date', 'duration_minutes', 'notes', 'status']
        read_only_fields = ['id', 'member', 'status']

# Serializer para que los entrenadores acepten una solicitud y creen la sesión
class TrainingSessionFromRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSession
        fields = ['date', 'duration_minutes', 'notes']