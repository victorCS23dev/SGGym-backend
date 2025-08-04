# memberships/serializers.py
from rest_framework import serializers
from .models import MembershipPlan, Membership

class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = ['id', 'name', 'description', 'price', 'duration_months', 'is_active']

class MembershipSerializer(serializers.ModelSerializer):
    plan = MembershipPlanSerializer(read_only=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Membership
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'status']
        read_only_fields = ['id', 'user', 'start_date', 'end_date', 'status']

class AdminMembershipSerializer(serializers.ModelSerializer):
    plan = MembershipPlanSerializer(read_only=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Membership
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'status']
        read_only_fields = ['id', 'user']

class MembershipPurchaseSerializer(serializers.Serializer):
    # Serializer para la compra de un plan. Solo necesita el ID del plan.
    plan_id = serializers.IntegerField()