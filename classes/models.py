from django.db import models
from users.models import User,Trainer_profile
from memberships.models import Membership_Plan

# Create your models here.
class class_type(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class gym_classes(models.Model):
    class_type = models.ForeignKey(class_type, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer_profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.TimeField()
    duration_minutes = models.IntegerField()
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.class_type.name} - {self.trainer.user.username} on {self.date.strftime("%Y-%m-%d")}'
    
    class Meta:
        unique_together = ('class_type', 'trainer', 'date', 'time') 
        ordering = ['date', 'time']

class class_membership_access(models.Model):
    gym_class = models.ForeignKey(gym_classes, on_delete=models.CASCADE)
    membership_plan = models.ForeignKey(Membership_Plan, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.gym_class} - {self.membership_plan.name}'
    
    class Meta:
        unique_together = ('gym_class', 'membership_plan')
        ordering = ['gym_class', 'membership_plan']

class class_reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(gym_classes, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} reserved {self.gym_class.class_type.name} on {self.gym_class.date.strftime("%Y-%m-%d")}'

    class Meta:
        unique_together = ('user', 'gym_class')
        ordering = ['-reservation_date']