import unittest
from unittest.mock import MagicMock, patch

from grpc_client.services.product import ProductService


class TestProductService(unittest.TestCase):

    @patch("grpc_client.services.product.product_pb2_grpc.ProductServiceStub")
    @patch("grpc_client.services.product.grpc.insecure_channel")
    def setUp(self, mock_channel, mock_stub_class):
        # Mock gRPC stub
        self.mock_stub = mock_stub_class.return_value
        self.service = ProductService(host="localhost", port=50051)

    def test_list_products(self):
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.name = "Laptop"
        mock_product.description = "Gaming Laptop"
        mock_product.price = 2000

        # Mock gRPC response
        mock_response = MagicMock()
        mock_response.products = [mock_product]
        self.mock_stub.ListProducts.return_value = mock_response

        response = self.service.list_products()
        self.assertEqual(len(response.products), 1)
        self.assertEqual(response.products[0].name, "Laptop")

    def test_get_product(self):
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.name = "Laptop"
        mock_product.description = "Gaming Laptop"
        mock_product.price = 2000

        self.mock_stub.GetProduct.return_value = mock_product
        response = self.service.get_product("1")
        self.assertEqual(response.id, "1")
        self.assertEqual(response.name, "Laptop")

    def test_create_product(self):
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.name = "Laptop"
        mock_product.description = "Gaming Laptop"
        mock_product.price = 2000

        self.mock_stub.CreateProduct.return_value = mock_product
        response = self.service.create_product("Laptop", "Gaming Laptop", 2000)
        self.assertEqual(response.id, "1")
        self.assertEqual(response.name, "Laptop")

    def test_update_product(self):
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.name = "Laptop Updated"
        mock_product.description = "Gaming Laptop Updated"
        mock_product.price = 2500

        self.mock_stub.UpdateProduct.return_value = mock_product
        response = self.service.update_product(
            "1", "Laptop Updated", "Gaming Laptop Updated", 2500
        )
        self.assertEqual(response.name, "Laptop Updated")
        self.assertEqual(response.price, 2500)

    def test_delete_product(self):
        mock_response = MagicMock()
        mock_response.id = "1"
        self.mock_stub.DeleteProduct.return_value = mock_response

        response = self.service.delete_product("1")
        self.assertEqual(response.id, "1")
