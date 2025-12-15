from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import User
from .serializers import UserSerializer
import logging

logger = logging.getLogger(__name__)

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        return User.objects.filter(id=user.id)

    def update(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id:
            logger.warning(
                f"User {request.user.username} tried to update another user"
            )
            raise PermissionDenied("You can only update your own account")
        return super().update(request, *args, **kwargs)

    

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            logger.warning(
                f"User {request.user.username} tried to delete a user"
            )
            raise PermissionDenied("Only admin can delete users")
        return super().destroy(request, *args, **kwargs)
