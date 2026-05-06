from rest_framework import status
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from cookie_cutter.users.models import User
from .serializers import UserSerializer
from .permissions import IsAdminOrSelf



class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]

    def get_queryset(self):
        """
        Admin → see all users
        Normal user → see only own profile
        """

        print("GETTING USER QUERYSET:", self.request)
        print("USER:", self.request.user)
        print("IS AUTH:", self.request.user.is_authenticated)

        user = self.request.user

        if user.is_staff:
            return User.objects.all()

        return User.objects.filter(id=user.id)
    
    def perform_create(self, serializer):
        """
        Only admin can create user
        """
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admin can create users")
        
        serializer.save()

    @action(detail=False, methods=["get"])
    def me(self, request):
        """
        GET /api/users/me/
        """
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
