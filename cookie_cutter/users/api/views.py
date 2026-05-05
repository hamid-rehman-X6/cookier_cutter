from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from cookie_cutter.users.models import User

from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """ViewSet for User CRUD operations.
    
    Provides full CRUD functionality:
    - CREATE: POST /api/users/
    - READ: GET /api/users/ (list) and GET /api/users/{id}/ (detail)
    - UPDATE: PUT /api/users/{id}/ (full) and PATCH /api/users/{id}/ (partial)
    - DELETE: DELETE /api/users/{id}/
    - CUSTOM: GET /api/users/me/ (current user)
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_permissions(self):
        """Allow unauthenticated users to create accounts only.

        Other actions remain protected by the default permission classes
        (configured in `REST_FRAMEWORK.DEFAULT_PERMISSION_CLASSES`).
        """
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Get current authenticated user profile."""
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
