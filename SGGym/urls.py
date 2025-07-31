from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.api import UserRegistrationView, CustomAuthToken, LogoutView, UserProfileViewSet, AdminUserManagementViewSet, TrainerProfileViewSet

router = routers.DefaultRouter()

# Registra solo los ViewSets con el router
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'admin-users', AdminUserManagementViewSet, basename='admin-users')
router.register(r'trainer-profile', TrainerProfileViewSet, basename='trainer-profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Registra las URLs que no usan ViewSets de forma individual
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    
    # Incluye las URLs generadas por el router
    path('api/', include(router.urls)),
]