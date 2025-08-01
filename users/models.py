from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

    ROLE_ADMIN = 'admin'
    ROLE_MEMBER = 'member'
    ROLE_TRAINER = 'trainer'

    ROLES_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MEMBER, 'Member'),
        (ROLE_TRAINER, 'Trainer')
    ]

    role = models.CharField(max_length=10, choices=ROLES_CHOICES, default=ROLE_MEMBER)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.username} ({self.role})'
    
    def save(self, *args, **kwargs):
        if self.role == self.ROLE_ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
    
class TrainerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Trainer Profile: {self.user.username}'