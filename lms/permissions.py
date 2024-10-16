from rest_framework.permissions import BasePermission


class IsOwnerOrModerator(BasePermission):
    """
    Разрешает доступ модераторам ко всем курсам, а пользователям — только к своим.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm('users.moderator'):
            # Модератору можно все, кроме удаления и создания
            if view.action in ['destroy', 'create']:
                return False
            return True


class IsOwner(BasePermission):
    """
    Разрешает доступ только владельцам объектов.
    """
    def has_object_permission(self, request, view, obj):
        # Доступ, если текущий пользователь - владелец объекта
        return obj == request.user or obj.autor == request.user
