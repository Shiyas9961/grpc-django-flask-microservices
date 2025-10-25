import grpc
from grpc_client.generated import product_pb2, product_pb2_grpc


class ProductService:
    def __init__(self, host="localhost", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = product_pb2_grpc.ProductServiceStub(self.channel)

    def create_product(self, name, description, price):
        request = product_pb2.ProductRequest(
            name=name, description=description, price=price
        )
        return self.stub.CreateProduct(request)

    def get_product(self, product_id):
        request = product_pb2.ProductId(id=product_id)
        return self.stub.GetProduct(request)

    def list_products(self):
        request = product_pb2.Empty()
        return self.stub.ListProducts(request)

    def update_product(self, product_id, name, description, price):
        request = product_pb2.ProductUpdateRequest(
            id=product_id, name=name, description=description, price=price
        )
        return self.stub.UpdateProduct(request)

    def delete_product(self, product_id):
        request = product_pb2.ProductId(id=product_id)
        return self.stub.DeleteProduct(request)
