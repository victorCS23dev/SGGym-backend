from .models import Membership_Plan, Membership
from rest_framework import viewsets, permissions
from .serializers import MembershipPlanSerializer, MembershipSerializer

class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = Membership_Plan.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    serializer_class = MembershipPlanSerializer

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    serializer_class = MembershipSerializer
