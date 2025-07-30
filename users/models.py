from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('trainer', 'Trainer'),], default='member')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} ({self.role})'
    
class Trainer_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Trainer Profile: {self.user.username}'