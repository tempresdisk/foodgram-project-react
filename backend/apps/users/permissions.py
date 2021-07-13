from rest_framework.permissions import IsAuthenticated


class AllowAnyAuthRetrieve(IsAuthenticated):
    def has_permission(self, request, view):
        if request.parser_context['kwargs'].get('pk', False):
            return super().has_permission(request, view)
        else:
            return True


class CurrentUserOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_superuser or obj.pk == user.pk
