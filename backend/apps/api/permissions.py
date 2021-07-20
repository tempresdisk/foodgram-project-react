from rest_framework import permissions


class AuthPostRetrieve(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS or \
           request.parser_context['kwargs'].get('pk', False):
            return super().has_permission(request, view)
        else:
            return True


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
