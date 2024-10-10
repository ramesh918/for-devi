# assignments/permissions.py

from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'