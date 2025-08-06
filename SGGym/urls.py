from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.api import (
    UserRegistrationView, CustomAuthToken, LogoutView, 
    UserProfileViewSet, AdminUserManagementViewSet, TrainerProfileViewSet, 
    TrainerProfileListView, TrainerActivitiesViewSet)
from payments.api import PaymentView, UserPaymentsView
from memberships.api import (
    MembershipPlanViewSet, MembershipViewSet, AdminMembershipPlanViewSet, 
    AdminMembershipViewSet
    )
from classes.api import (
    ClassTypeViewSet, AdminClassTypeViewSet, AdminGymClassViewSet, 
    GymClassViewSet, UserGymClassViewSet, AdminClassMembershipAccessViewSet
    )
from trainings.api import (
    AdminTrainingTypeViewSet, TrainingTypeViewSet, AdminTrainingSessionViewSet,
    TrainingSessionViewSet, TrainingRequestViewSet
    )

router = routers.DefaultRouter()

# Registra solo los ViewSets con el router
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'admin-users', AdminUserManagementViewSet, basename='admin-users')
router.register(r'trainer-profile', TrainerProfileViewSet, basename='trainer-profile')
router.register(r'trainer-profile-list', TrainerProfileListView, basename='trainer-profile-list')
router.register(r'trainer-activities', TrainerActivitiesViewSet, basename='trainer-activities')
router.register(r'membership-plans', MembershipPlanViewSet, basename='membership-plans')
router.register(r'admin-membership-plans', AdminMembershipPlanViewSet, basename='admin-membership-plans')
router.register(r'membership', MembershipViewSet, basename='membership')
router.register(r'admin-membership', AdminMembershipViewSet, basename='admin-membership')
router.register(r'class-types', ClassTypeViewSet, basename='class-types')
router.register(r'admin-class-types', AdminClassTypeViewSet, basename='admin-class-types')
router.register(r'gym-classes', GymClassViewSet, basename='gym-classes')
router.register(r'admin-gym-classes', AdminGymClassViewSet, basename='admin-gym-classes')
router.register(r'user-gym-classes', UserGymClassViewSet, basename='user-gym-classes')
router.register(r'admin-class-membership-access', AdminClassMembershipAccessViewSet, basename='admin-class-membership-access')
router.register(r'admin-training-types', AdminTrainingTypeViewSet, basename='admin-training-types')
router.register(r'training-types', TrainingTypeViewSet, basename='training-types')
router.register(r'admin-training-sessions', AdminTrainingSessionViewSet, basename='admin-training-sessions')
router.register(r'training-sessions', TrainingSessionViewSet, basename='training-sessions')
router.register(r'training-requests', TrainingRequestViewSet, basename='training-requests')
router.register(r'payments', UserPaymentsView, basename='payments')
router.register(r'admin-payment', PaymentView, basename='admin-payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Registra las URLs que no usan ViewSets de forma individual
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    # Incluye las URLs generadas por el router
    path('api/', include(router.urls)),
]