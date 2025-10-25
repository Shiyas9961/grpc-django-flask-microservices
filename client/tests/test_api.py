import unittest
from unittest.mock import MagicMock, patch

from apis.product import product_bp
from flask import Flask


class TestProductAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(product_bp)
        self.client = self.app.test_client()

    @patch("apis.product.grpc_product_service")
    def test_list_products(self, mock_service):
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

    @patch("apis.product.grpc_product_service")
    def test_create_product_missing_fields(self, mock_service):
        response = self.client.post("/products", json={"name": "Laptop"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.json["error"])

    @patch("apis.product.grpc_product_service")
    def test_update_product(self, mock_service):
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.name = "Laptop Updated"
        mock_product.description = "Gaming Laptop Updated"
        mock_product.price = 2500
        mock_service.update_product.return_value = mock_product

        response = self.client.put(
            "/products/1",
            json={
                "name": "Laptop Updated",
                "description": "Gaming Laptop Updated",
                "price": 2500,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {
                "id": "1",
                "name": "Laptop Updated",
                "description": "Gaming Laptop Updated",
                "price": 2500,
            },
        )

    @patch("apis.product.grpc_product_service")
    def test_delete_product(self, mock_service):
        mock_response = MagicMock()
        mock_response.id = "1"
        mock_service.delete_product.return_value = mock_response

        response = self.client.delete("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"deleted_id": "1"})
