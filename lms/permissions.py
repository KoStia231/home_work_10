from rest_framework.permissions import BasePermission


class IsOwnerOrModerator(BasePermission):
    """
    Разрешает доступ только модераторам или владельцам объектов.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm('users.moderator'):
            return True
        return obj.author == request.user
