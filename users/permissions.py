# users/permissions.py
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado que solo permite el acceso a los usuarios con el rol 'admin'.
    """
    def has_permission(self, request, view):
        # Primero, verifica si el usuario está autenticado. Si no lo está, no puede tener un rol.
        # Luego, verifica que el rol del usuario sea 'admin'.
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsTrainer(permissions.BasePermission):
    """
    Permiso personalizado que solo permite el acceso a los usuarios con el rol 'trainer'.
    """
    def has_permission(self, request, view):
        # Primero, verifica si el usuario está autenticado.
        # Luego, verifica que el rol del usuario sea 'trainer'.
        return bool(request.user and request.user.is_authenticated and request.user.role == 'trainer')
        
class IsMember(permissions.BasePermission):
    """
    Permiso personalizado que solo permite el acceso a los usuarios con el rol 'member'.
    """
    def has_permission(self, request, view):
        # Primero, verifica si el usuario está autenticado.
        # Luego, verifica que el rol del usuario sea 'member'.
        return bool(request.user and request.user.is_authenticated and request.user.role == 'member')