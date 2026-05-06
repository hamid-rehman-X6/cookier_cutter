from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSelf(BasePermission):
    """
    Admin → full access
    User → only own data (read, update, delete)
    """

    def has_permission(self, request, view):
        # Authentication required
        request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_staff:
            return True

        # User can only access their own object
        return obj == request.user
