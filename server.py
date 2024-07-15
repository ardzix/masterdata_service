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
from catalogue.grpc import catalogue_pb2_grpc
from catalogue.grpc.grpc_services import ProductService
from channel.grpc import channel_pb2_grpc
from channel.grpc.grpc_services import ChannelService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add both PointService and PromoService to the same server instance
    catalogue_pb2_grpc.add_CatalogueServiceServicer_to_server(ProductService(), server)
    channel_pb2_grpc.add_ChannelServiceServicer_to_server(ChannelService(), server)

    # Listen on two different ports
    server.add_insecure_port(f'[::]:{settings.MD_CATALOGUE_SERVICE_PORT}')
    server.add_insecure_port(f'[::]:{settings.MD_CHANNEL_SERVICE_PORT}')

    server.start()
    print(f'gRPC servers running on ports {settings.MD_CATALOGUE_SERVICE_PORT} and {settings.MD_CHANNEL_SERVICE_PORT}...')
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
