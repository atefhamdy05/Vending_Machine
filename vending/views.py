from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vending.permissions import IsBuyer
from products.models import Product

VALID_COINS = [5, 10, 20, 50, 100]


class Deposit(APIView):
    permission_classes = [IsBuyer]

    def post(self, request):
        coin =int( request.data.get('coin'))

        if coin not in VALID_COINS:
            return Response({"error": "Invalid coin"}, status=400)

        request.user.deposit += coin
        request.user.save()
        return Response({"deposit": request.user.deposit})


class Buy(APIView):
    permission_classes = [IsBuyer]

    def post(self, request):
        product_name = request.data.get('productName')
        amount = int(request.data.get('amount', 0))

        try:
            product = Product.objects.get(productName=product_name)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        
        total_cost = product.cost * amount

        if product.amountAvailable < amount:
            return Response({"error": "Not enough stock"}, status=400)

        if request.user.deposit < total_cost:
            return Response({"error": "Insufficient balance"}, status=400)

        product.amountAvailable -= amount
        product.save()

        request.user.deposit -= total_cost
        change = request.user.deposit
        request.user.deposit = 0
        request.user.save()

        return Response({
            "total_spent": total_cost,
            "product": product.productName,
            "amount": amount,
            "change": calculate_change(change)
        })
class Reset(APIView):
    permission_classes = [IsBuyer]

    def post(self, request):
        request.user.deposit = 0
        request.user.save()
        return Response({"message": "Deposit reset"})
    
    
def calculate_change(change):
    coins = {}
    for coin in sorted(VALID_COINS, reverse=True):
        coins[coin], change = divmod(change, coin)
    return coins
