from apps.products.models import Product
from django.test import TestCase


class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            name="Test Product", description="Test Description", price=100.50
        )

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(str(product), "Test Product")
        self.assertIsNotNone(product.id)
