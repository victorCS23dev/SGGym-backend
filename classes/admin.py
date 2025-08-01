from django.contrib import admin
from .models import ClassType, GymClass, ClassReservation, ClassMembershipAccess
# Register your models here.
admin.site.register(ClassType)
admin.site.register(GymClass)
admin.site.register(ClassReservation)
admin.site.register(ClassMembershipAccess)
