from django.db import models
from users.models import User, Trainer_profile

# Create your models here.
class Training_types(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name    
    
class Training_sessions(models.Model):
    training_type = models.ForeignKey(Training_types, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer_profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_sessions')
    date = models.DateTimeField()
    time = models.TimeField()
    duration_minutes = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.training_type.name} - {self.trainer.user.username} on {self.date.strftime("%Y-%m-%d")}'
    
    class Meta:
        unique_together = ('training_type', 'trainer', 'date', 'time') 
        ordering = ['date', 'time']