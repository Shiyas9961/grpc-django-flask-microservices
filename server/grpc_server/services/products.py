import logging

import grpc
from apps.products.models import Product
from django.core.exceptions import ObjectDoesNotExist
from grpc_server.generated import product_pb2, product_pb2_grpc

# ✅ Get custom logger
logger = logging.getLogger("grpc_server")


class ProductService(product_pb2_grpc.ProductServiceServicer):
    def CreateProduct(self, request, context):
        logger.info("Creating product...")
        product = Product.objects.create(
            name=request.name,
            description=request.description,
            price=request.price,
        )
        logger.info(f"Product created: {product}")
        return product_pb2.ProductResponse(
            id=str(product.id),
            name=product.name,
            description=product.description,
            price=float(product.price),
        )

    def GetProduct(self, request, context):
        try:
            logger.info(f"Getting product with id={request.id}")
            product = Product.objects.get(id=request.id)
            logger.info(f"Product found: {product}")
            return product_pb2.ProductResponse(
                id=str(product.id),
                name=product.name,
                description=product.description,
                price=float(product.price),
            )
        except ObjectDoesNotExist:
            logger.warning(f"Product not found with id={request.id}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.ProductResponse()

    def ListProducts(self, request, context):
        logger.info("Listing products...")
        products = Product.objects.all()
        resp = product_pb2.ProductList()
        for p in products:
            resp.products.add(
                id=str(p.id),
                name=p.name,
                description=p.description,
                price=float(p.price),
            )
        logger.info(f"Found {products.count()} products")
        return resp

    def UpdateProduct(self, request, context):
        try:
            logger.info(f"Updating product with id={request.id}")
            product = Product.objects.get(id=request.id)
            if request.name:
                product.name = request.name
            if request.description:
                product.description = request.description
            if request.price:
                product.price = request.price
            product.save()
            logger.info(f"Product updated: {product}")
            return product_pb2.ProductResponse(
                id=str(product.id),
                name=product.name,
                description=product.description,
                price=float(product.price),
            )
        except Product.DoesNotExist:
            logger.warning(f"Product not found for update id={request.id}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.ProductResponse()

    def DeleteProduct(self, request, context):
        try:
            logger.info(f"Deleting product with id={request.id}")
            product = Product.objects.get(id=request.id)
            product_id = product.id
            product.delete()
            logger.info(f"Product deleted with id={product_id}")
            return product_pb2.DeleteResponse(id=str(product_id))
        except Product.DoesNotExist:
            logger.warning(f"Product not found for delete id={request.id}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.DeleteResponse()
