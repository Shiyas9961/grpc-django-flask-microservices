import unittest
from unittest.mock import MagicMock, patch

from apis.product import product_bp
from flask import Flask


class TestProductAPI(unittest.TestCase):
    def setUp(self):
        # create Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(product_bp)
        self.client = self.app.test_client()

    @patch("apis.product.grpc_product_service")
    def test_list_products(self, mock_service):
        # Mock the gRPC response
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.name = "Laptop"
        mock_product.description = "Gaming Laptop"
        mock_product.price = 2000
        mock_service.list_products.return_value.products = [mock_product]

        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {
                    "id": "1",
                    "name": "Laptop",
                    "description": "Gaming Laptop",
                    "price": 2000,
                }
            ],
        )

    @patch("apis.product.grpc_product_service")
    def test_get_product(self, mock_service):
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.name = "Laptop"
        mock_product.description = "Gaming Laptop"
        mock_product.price = 2000
        mock_service.get_product.return_value = mock_product

        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {
                "id": "1",
                "name": "Laptop",
                "description": "Gaming Laptop",
                "price": 2000,
            },
        )

    @patch("apis.product.grpc_product_service")
    def test_create_product(self, mock_service):
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.name = "Laptop"
        mock_product.description = "Gaming Laptop"
        mock_product.price = 2000
        mock_service.create_product.return_value = mock_product

        response = self.client.post(
            "/products",
            json={
                "name": "Laptop",
                "description": "Gaming Laptop",
                "price": 2000,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {
                "id": "1",
                "name": "Laptop",
                "description": "Gaming Laptop",
                "price": 2000,
            },
        )


if __name__ == "__main__":
    unittest.main()
