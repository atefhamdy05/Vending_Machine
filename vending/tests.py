# users/tests.py or tests.py at project root
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from products.models import Product

class VendingMachineAPITests(APITestCase):

    def setUp(self):
        # Create a buyer and a seller
        self.buyer = User.objects.create_user(username="buyer1", password="pass123", role="buyer")
        self.seller = User.objects.create_user(username="seller1", password="pass123", role="seller")
        self.admin = User.objects.create_superuser(username="admin", password="pass123")

        # Authenticate seller for product creation
        resp = self.client.post(reverse('token_obtain_pair'), {"username": "seller1", "password": "pass123"})
        self.seller_token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.seller_token}')

        # Create a product
        self.product = Product.objects.create(
            productName="Cola",
            cost=10,
            amountAvailable=5,
            seller=self.seller
        )

    def test_buyer_cannot_create_product(self):
        self.client.credentials()  # remove previous token
        resp = self.client.post(reverse('token_obtain_pair'), {"username": "buyer1", "password": "pass123"})
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {"productName": "Pepsi", "cost": 10, "amountAvailable": 5}
        resp = self.client.post("/api/products/", data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_can_create_product(self):
        data = {"productName": "Pepsi", "cost": 10, "amountAvailable": 5}
        resp = self.client.post("/api/products/", data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['seller'], self.seller.id)

    def test_buyer_deposit_and_buy(self):
        # Deposit
        self.client.credentials()  # remove previous token
        resp = self.client.post(reverse('token_obtain_pair'), {"username": "buyer1", "password": "pass123"})
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        resp = self.client.post("/api/deposit/", {"coin": 20})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['deposit'], 20)

        # Buy product
        resp = self.client.post("/api/buy/", {"productName": self.product.productName, "amount": 1})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("total_spent", resp.data)
        self.assertIn("change", resp.data)

    

  