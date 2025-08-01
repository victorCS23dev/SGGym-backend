from django.db import models
from users.models import CustomUser,TrainerProfile
from memberships.models import MembershipPlan

# Create your models here.
class ClassType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class GymClass(models.Model):
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.DurationField()
    max_participants = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f'{self.class_type.name} by {self.trainer.user.username}'

class ClassReservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'gym_class')
    
    def __str__(self):
        return f'{self.user.username} reserved {self.gym_class.class_type.name}'

class ClassMembershipAccess(models.Model):
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('membership_plan', 'class_type')
    
    def __str__(self):
        return f'{self.membership_plan.name} access to {self.class_type.name}'

