from django.contrib import admin
from .models import CustomUser, TrainerProfile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(TrainerProfile)