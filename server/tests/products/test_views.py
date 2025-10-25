from apps.products.models import Product
from django.urls import reverse
from rest_framework.test import APITestCase


class ProductListAPIViewTest(APITestCase):
    def setUp(self):
        Product.objects.all().delete()
        self.product = Product.objects.create(
            name="Laptop", description="Gaming Laptop", price=2000
        )

    def test_list_products(self):
        url = reverse("product-list")
        response = self.client.get(url)

        # Debug: Print what we're actually getting
        print(f"Response status: {response.status_code}")
        print(f"Response data type: {type(response.data)}")
        print(f"Response data: {response.data}")

        self.assertEqual(response.status_code, 200)

        # If response.data is paginated, it will be a dict with 'results' key
        if isinstance(response.data, dict):
            # Paginated response
            products = response.data.get("results", [])
        else:
            # Non-paginated response
            products = response.data

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Laptop")
        self.assertEqual(products[0]["description"], "Gaming Laptop")
