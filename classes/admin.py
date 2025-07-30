from django.contrib import admin
from .models import class_type, gym_classes, class_membership_access, class_reservation
# Register your models here.
admin.site.register(class_type)
admin.site.register(gym_classes)
admin.site.register(class_membership_access)
admin.site.register(class_reservation)