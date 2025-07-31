from .models import class_type, gym_classes, class_membership_access, class_reservation
from rest_framework import viewsets, permissions
from .serializers import ClassTypeSerializer, GymClassSerializer, ClassMembershipAccessSerializer, ClassReservationSerializer

class ClassTypeViewSet(viewsets.ModelViewSet):
    queryset = class_type.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    serializer_class = ClassTypeSerializer

class GymClassViewSet(viewsets.ModelViewSet):
    queryset = gym_classes.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    serializer_class = GymClassSerializer

class ClassMembershipAccessViewSet(viewsets.ModelViewSet):
    queryset = class_membership_access.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    serializer_class = ClassMembershipAccessSerializer

class ClassReservationViewSet(viewsets.ModelViewSet):
    queryset = class_reservation.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    serializer_class = ClassReservationSerializer