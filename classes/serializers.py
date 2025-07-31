from rest_framework import serializers
from .models import class_type, gym_classes, class_membership_access, class_reservation

class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = class_type
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)

class GymClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = gym_classes
        fields = ('id', 'class_type', 'trainer', 'date', 'time', 'duration_minutes', 'capacity', 'is_active')
        read_only_fields = ('id',)

class ClassMembershipAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = class_membership_access
        fields = ('id', 'gym_class', 'membership_plan')
        read_only_fields = ('id',)

class ClassReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = class_reservation
        fields = ('id', 'user', 'gym_class', 'reservation_date')
        read_only_fields = ('id',)