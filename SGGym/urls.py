from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.api import UserRegistrationView, CustomAuthToken, LogoutView, UserProfileViewSet, AdminUserManagementViewSet, TrainerProfileViewSet
from payments.api import PaymentView
from memberships.api import MembershipPlanViewSet, MembershipViewSet, AdminMembershipPlanViewSet

router = routers.DefaultRouter()

# Registra solo los ViewSets con el router
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'admin-users', AdminUserManagementViewSet, basename='admin-users')
router.register(r'trainer-profile', TrainerProfileViewSet, basename='trainer-profile')
router.register(r'membership-plans', MembershipPlanViewSet, basename='membership-plans')
router.register(r'admin-membership-plans', AdminMembershipPlanViewSet, basename='admin-membership-plans')
router.register(r'membership', MembershipViewSet, basename='membership')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Registra las URLs que no usan ViewSets de forma individual
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/payment/', PaymentView.as_view(), name='payment'),

    # Incluye las URLs generadas por el router
    path('api/', include(router.urls)),
]