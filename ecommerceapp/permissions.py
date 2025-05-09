from rest_framework import permissions


class IsActiveEmployeePermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_active: # and request.user.is_staff
            return True
        return False