import os
import sys
import time
from concurrent import futures

import grpc

# Setup Django environment for model access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django  # noqa: E402

django.setup()

from grpc_server.generated import product_pb2_grpc  # noqa: E402
from services import products as product_service  # noqa: E402


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        product_service.ProductService(), server
    )

    server.add_insecure_port("[::]:50051")
    print("🚀 gRPC server running on port 50051...")
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down gRPC server...")
        server.stop(0)


if __name__ == "__main__":
    serve()
