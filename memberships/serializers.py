from rest_framework import serializers
from .models import Membership_Plan, Membership

class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership_Plan
        fields = ['id', 'name', 'description', 'price', 'duration_months', 'created_at']
        read_only_fields = ['id', 'created_at']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'is_active']
