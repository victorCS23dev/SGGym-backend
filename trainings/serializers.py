from rest_framework import serializers
from .models import TrainingType, TrainingSession
from users.serializers import UserProfileSerializer, TrainerProfileSerializer

class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = ['id', 'name', 'description']

class TrainingSessionSerializer(serializers.ModelSerializer):
    training_type = TrainingTypeSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    trainer = TrainerProfileSerializer(read_only=True)
    # Campo de solo escritura para que el frontend envíe el ID
    training_type_id = serializers.IntegerField(write_only=True)
    trainer_id = serializers.IntegerField(write_only=True, required=False)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = TrainingSession
        fields = [
            'id', 'user', 'user_id', 'trainer', 'trainer_id',
            'training_type', 'training_type_id',
            'date', 'duration_minutes', 'notes'
        ]

class TrainingSessionCreateSerializer(serializers.ModelSerializer):
    training_type_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = TrainingSession
        fields = ['training_type_id', 'date', 'duration_minutes', 'notes']