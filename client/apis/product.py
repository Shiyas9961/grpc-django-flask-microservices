from config.settings import get_config
from flask import Blueprint, jsonify, request
from grpc_client.services.product import ProductService

grpc_product_service = ProductService(
    host=get_config().GRPC_HOST, port=get_config().GRPC_PORT
)
product_bp = Blueprint("product_bp", __name__)


@product_bp.route("/products", methods=["GET"])
def list_products():
    try:
        response = grpc_product_service.list_products()
        products = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
            }
            for p in response.products
        ]
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_bp.route("/products", methods=["POST"])
def create_product():
    data = request.json
    name = data.get("name")
    desc = data.get("description")
    price = data.get("price")
    if not name or not desc or not price:
        return jsonify({"error": "Missing required fields"}), 400
    try:
        response = grpc_product_service.create_product(
            data["name"],
            data["description"],
            data["price"],
        )
        return jsonify(
            {
                "id": response.id,
                "name": response.name,
                "description": response.description,
                "price": response.price,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_bp.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        response = grpc_product_service.get_product(product_id)
        return jsonify(
            {
                "id": response.id,
                "name": response.name,
                "description": response.description,
                "price": response.price,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_bp.route("/products/<string:product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        data = request.json
        response = grpc_product_service.update_product(
            product_id,
            data["name"],
            data["description"],
            data["price"],
        )
        return jsonify(
            {
                "id": response.id,
                "name": response.name,
                "description": response.description,
                "price": response.price,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_bp.route("/products/<string:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        response = grpc_product_service.delete_product(product_id)
        return jsonify({"deleted_id": response.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
