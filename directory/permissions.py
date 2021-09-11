from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model


User = get_user_model()


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.ADMIN


