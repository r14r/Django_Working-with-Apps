from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import TodoItem
from .serializers import TodoItemSerializer


class IsEmailVerified(permissions.BasePermission):
    """Allow access only to users with a verified email address."""

    message = 'E-Mail-Adresse nicht bestätigt.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'email_verified', True)
        )


class TodoItemViewSet(viewsets.ModelViewSet):
    serializer_class = TodoItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def get_queryset(self):
        return TodoItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied()
        instance.delete()
