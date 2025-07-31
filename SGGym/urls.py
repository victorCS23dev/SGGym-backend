"""
URL configuration for SGGym project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.api import UserViewSet, TrainerProfileViewSet
from trainings.api import TrainingTypeViewSet, TrainingSessionViewSet
from memberships.api import MembershipPlanViewSet, MembershipViewSet
from classes.api import ClassTypeViewSet, GymClassViewSet, ClassMembershipAccessViewSet, ClassReservationViewSet

router = routers.DefaultRouter()
router.register('api/users', UserViewSet, 'user')
router.register('api/trainer-profiles', TrainerProfileViewSet, 'trainer-profile')
router.register('api/training-types', TrainingTypeViewSet, 'training-type')
router.register('api/training-sessions', TrainingSessionViewSet, 'training-session')
router.register('api/membership-plans', MembershipPlanViewSet, 'membership-plan')
router.register('api/memberships', MembershipViewSet, 'membership')
router.register('api/class-types', ClassTypeViewSet, 'class-type')
router.register('api/gym-classes', GymClassViewSet, 'gym-class')
router.register('api/class-membership-access', ClassMembershipAccessViewSet, 'class-membership-access')
router.register('api/class-reservations', ClassReservationViewSet, 'class-reservation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
