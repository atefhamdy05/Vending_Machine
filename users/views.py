from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import User
from .serializers import UserSerializer
import logging
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    #determind the permission of the viewswt in case it create or else 
    def get_permissions(self):
        if self.action == 'create':
            if self.request.user.is_authenticated:
                raise PermissionDenied("Authenticated users cannot create new accounts")
            return [AllowAny()]

        return [IsAuthenticated()]
    
    #Create the user 
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            role=serializer.validated_data['role'],
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
        
        
    #Get all the users in case admin and in case the user is seller or buyer return his information only
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        return User.objects.filter(id=user.id)
    
    
    #each user can updated his information only 
    def update(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id:
            logger.warning(
                f"User {request.user.username} tried to update another user"
            )
            raise PermissionDenied("You can only update your own account")
        return super().update(request, *args, **kwargs)

    
    #Only Admin Can delete the user 
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            logger.warning(
                f"User {request.user.username} tried to delete a user"
            )
            raise PermissionDenied("Only admin can delete users")
        return super().destroy(request, *args, **kwargs)
