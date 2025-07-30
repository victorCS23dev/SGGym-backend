from rest_framework import serializers
from .models import Training_types, Training_sessions

class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_types
        fields = ['id', 'name', 'description']

class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_sessions
        fields = ['id', 'training_type', 'trainer', 'user', 'date', 'time', 'duration_minutes', 'is_active']