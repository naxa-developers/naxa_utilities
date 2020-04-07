from rest_framework.permissions import BasePermission


class IsFrontendUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        authenticated = bool(request.user and request.user.is_authenticated)
        if not authenticated:
            return authenticated
        frontend_group = request.user.roles.filter(
            group__name="FrontEnd").exists()
        return frontend_group
