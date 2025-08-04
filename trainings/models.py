from django.db import models
from users.models import CustomUser, TrainerProfile
# Create your models here.
class TrainingType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class TrainingSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='training_sessions')
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, related_name='training_sessions')
    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    notes = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f'{self.user.username} - {self.training_type.name} on {self.date.strftime("%Y-%m-%d %H:%M")}'