import grpc
import grpc_server.generated.product_pb2 as product_pb2
from apps.products.models import Product
from django.test import TestCase
from grpc_server.services.products import ProductService


# A fake context to mimic grpc.ServicerContext
class FakeContext:
    def __init__(self):
        self.code = None
        self.details_msg = None

    def set_code(self, code):
        self.code = code

    def set_details(self, msg):
        self.details_msg = msg


class ProductServiceTest(TestCase):
    def setUp(self):
        self.service = ProductService()

    def test_create_product(self):
        request = product_pb2.ProductRequest(
            name="Laptop",
            description="Gaming Laptop",
            price=1200.50,
        )
        context = FakeContext()
        response = self.service.CreateProduct(request, context)

        self.assertIsNotNone(response.id)
        self.assertEqual(response.name, "Laptop")
        self.assertEqual(response.description, "Gaming Laptop")
        self.assertEqual(float(response.price), 1200.50)
        self.assertTrue(Product.objects.filter(id=response.id).exists())

    def test_get_product_success(self):
        product = Product.objects.create(
            name="Phone", description="Android", price=599.99
        )
        request = product_pb2.ProductId(id=str(product.id))
        context = FakeContext()
        response = self.service.GetProduct(request, context)

        self.assertEqual(response.id, str(product.id))
        self.assertEqual(response.name, "Phone")
        self.assertIsNone(context.code)  # No error

    def test_get_product_not_found(self):
        request = product_pb2.ProductId(
            id="00000000-0000-0000-0000-000000000000",
        )
        context = FakeContext()
        response = self.service.GetProduct(request, context)

        self.assertEqual(
            context.code,
            grpc.StatusCode.NOT_FOUND,
        )
        self.assertEqual(response.id, "")

    def test_list_products(self):
        Product.objects.create(
            name="A",
            description="Test A",
            price=100,
        )
        Product.objects.create(
            name="B",
            description="Test B",
            price=200,
        )
        request = product_pb2.Empty()
        context = FakeContext()
        response = self.service.ListProducts(request, context)

        self.assertEqual(len(response.products), 2)
        names = [p.name for p in response.products]
        self.assertIn("A", names)
        self.assertIn("B", names)

    def test_update_product(self):
        product = Product.objects.create(
            name="Old",
            description="Old Desc",
            price=100,
        )
        request = product_pb2.ProductUpdateRequest(
            id=str(product.id),
            name="New",
            description="New Desc",
            price=200,
        )
        context = FakeContext()
        response = self.service.UpdateProduct(request, context)

        self.assertEqual(response.name, "New")
        self.assertEqual(float(response.price), 200.0)
        updated = Product.objects.get(id=product.id)
        self.assertEqual(updated.name, "New")

    def test_update_product_not_found(self):
        request = product_pb2.ProductUpdateRequest(
            id="00000000-0000-0000-0000-000000000000",
            name="X",
            description="X",
            price=100,
        )
        context = FakeContext()
        response = self.service.UpdateProduct(request, context)

        self.assertEqual(
            context.code,
            grpc.StatusCode.NOT_FOUND,
        )
        self.assertEqual(response.id, "")

    def test_delete_product(self):
        product = Product.objects.create(
            name="DeleteMe",
            description="Temp",
            price=300,
        )
        request = product_pb2.ProductId(id=str(product.id))
        context = FakeContext()
        response = self.service.DeleteProduct(request, context)

        self.assertEqual(response.id, str(product.id))
        self.assertFalse(Product.objects.filter(id=product.id).exists())

    def test_delete_product_not_found(self):
        request = product_pb2.ProductId(
            id="00000000-0000-0000-0000-000000000000",
        )
        context = FakeContext()
        response = self.service.DeleteProduct(request, context)

        self.assertEqual(
            context.code,
            grpc.StatusCode.NOT_FOUND,
        )
        self.assertEqual(response.id, "")
