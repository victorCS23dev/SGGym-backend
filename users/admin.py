from django.contrib import admin
from .models import CustomUser, Trainer_profile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Trainer_profile)