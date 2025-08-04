from rest_framework import serializers
from .models import ClassType, GymClass, ClassReservation, ClassMembershipAccess
from users.models import TrainerProfile
from users.serializers import UserProfileSerializer

class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassType
        fields = ['id', 'name', 'description']

class GymClassSerializer(serializers.ModelSerializer):
    class_type = ClassTypeSerializer(read_only=True)
    trainer = UserProfileSerializer(read_only=True)
    # Campo de solo escritura para que el frontend envíe el ID
    class_type_id = serializers.IntegerField(write_only=True)
    trainer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = GymClass
        fields = [
            'id', 'class_type', 'class_type_id', 'trainer', 'trainer_id',
            'date', 'duration', 'max_participants'
        ]
    
class ClassReservationSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    gym_class = GymClassSerializer(read_only=True)

    class Meta:
        model = ClassReservation
        fields = ['id', 'user', 'gym_class', 'reservation_date']

class ClassReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassReservation
        fields = ['gym_class']

class ClassMembershipAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMembershipAccess
        fields = ['id', 'membership_plan', 'class_type']

