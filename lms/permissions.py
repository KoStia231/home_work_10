from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        return request.user.has_perm('users.moderator')


class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь автором объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.autor == request.user
