from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from django.test import TestCase


class ProductSerializerTest(TestCase):
    def test_serializer_data(self):
        product = Product.objects.create(
            name="Phone", description="Smartphone", price=999.99
        )
        serializer = ProductSerializer(product)
        data = serializer.data

        self.assertEqual(data["name"], "Phone")
        self.assertEqual(float(data["price"]), 999.99)
