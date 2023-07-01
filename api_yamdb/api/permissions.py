from rest_framework import permissions
# from rest_framework.permissions import BasePermission
# # В моделях нет Comment и Review
# from reviews.models import ROLE_LIST, Comment, Review, User


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        ):
            return True


class AdminModeratorAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


# Добавил своё, хз правильно или нет
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated


# Прописать IsAuthorPermission!!!!
class IsAuthorPermission(permissions.BasePermission):
    pass
