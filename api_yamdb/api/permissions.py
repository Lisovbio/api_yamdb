from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Если запрос не get, head, options,
    то права даются только админу'''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)
