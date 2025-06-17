# store/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, Category, Product
from rest_framework.test import APIClient
from rest_framework import status


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="seller1", password="test1234")
        self.profile = UserProfile.objects.create(user=self.user, is_seller=True)
        self.category = Category.objects.create(name="Clothing")

    def test_create_product(self):
        product = Product.objects.create(
            name="T-shirt",
            description="Cool cotton t-shirt",
            price=200,
            seller=self.profile,
            category=self.category,
            condition="new",
            is_available=True,
        )
        self.assertEqual(str(product.name), "T-shirt")
        self.assertEqual(product.price, 200)


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="apiuser", password="pass1234")
        self.profile = UserProfile.objects.create(user=self.user, is_seller=True)
        self.category = Category.objects.create(name="Electronics")

    def test_product_list_endpoint(self):
        # Create a product to be listed
        Product.objects.create(
            name="Laptop",
            description="Used laptop",
            price=500,
            seller=self.profile,
            category=self.category,
            condition="used",
            is_available=True,
        )

        response = self.client.get('/api/products/')  # Make sure this matches your URLConf
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "password": "test1234",
            "email": "newuser@example.com"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
