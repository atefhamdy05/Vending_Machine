from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer
from rest_framework.exceptions import PermissionDenied
from vending.permissions import IsSeller
import logging
logger = logging.getLogger(__name__)
class ProductViewSet(ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] #all users can see the products

    #Only Sellers can create product 
    def perform_create(self, serializer):
        if self.request.user.role != 'seller':
            raise PermissionDenied("You Are Not A Seller")
        serializer.save(seller=self.request.user)
        
    #Only the seller can update and delete his own product 
    def perform_update(self, serializer):
        product = self.get_object()
        if product.seller != self.request.user:
            logger.warning(f"User {self.request.user} tried to update product {product.id}")
            raise PermissionDenied("Not your product")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.seller != self.request.user:
            logger.warning(f"User {self.request.user} tried to delete product {instance.id}")
            raise PermissionDenied("Not your product")
        instance.delete()
