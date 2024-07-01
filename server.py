# server.py
import os
import grpc
from concurrent import futures
import time

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masterdata.settings')

import django
django.setup()

from django.conf import settings
from proto import masterdata_pb2_grpc
from service.grpc_services import ProductService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    masterdata_pb2_grpc.add_MasterDataServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
