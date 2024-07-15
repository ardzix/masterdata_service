import grpc
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masterdata.settings')
django.setup()

from django.conf import settings
import uuid
from google.protobuf import empty_pb2
from catalogue.grpc import catalogue_pb2, catalogue_pb2_grpc

def print_product(product):
    print(f"hash: {product.hash}")
    print(f"name: {product.name}")
    print(f"description: {product.description}")
    print(f"category_id: {product.category_id}")
    print(f"brand_id: {product.brand_id}")
    print(f"base_price: {product.base_price}")
    print(f"stock: {product.stock}")
    print(f"sku: {product.sku}")
    print(f"weight: {product.weight}")
    print(f"dimensions: {product.dimensions}")
    print(f"is_active: {product.is_active}")
    print("images:")
    for image in product.images:
        print(f"  - url: {image.image_url}, alt_text: {image.alt_text}, is_primary: {image.is_primary}")
    print("attributes:")
    for attribute in product.attributes:
        print(f"  - {attribute.name}: {attribute.value}")
    print("variants:")
    for variant in product.variants:
        print(f"  - name: {variant.name}, attributes: {variant.attributes}, price: {variant.price}, stock: {variant.stock}, sku: {variant.sku}, image_url: {variant.image_url}, hash: {variant.hash}")

def run():
    with grpc.insecure_channel(f'{settings.MD_CATALOGUE_SERVICE_HOST}:{settings.MD_CATALOGUE_SERVICE_PORT}') as channel:
        stub = catalogue_pb2_grpc.CatalogueServiceStub(channel)

        # Create a new product
        create_request = catalogue_pb2.CreateProductRequest(
            name="Test Product",
            description="A product for testing",
            category_id=1,
            brand_id=1,
            base_price=100.0,
            stock=10,
            sku="TESTSKU",
            weight=0.5,
            dimensions="10x10x10",
            is_active=True,
            hash=str(uuid.uuid4()),
            images=[
                catalogue_pb2.ProductImage(
                    image_url="http://example.com/image1.jpg",
                    alt_text="Image 1",
                    is_primary=True
                ),
                catalogue_pb2.ProductImage(
                    image_url="http://example.com/image2.jpg",
                    alt_text="Image 2",
                    is_primary=False
                )
            ],
            attributes=[
                catalogue_pb2.ProductAttribute(
                    name="Color",
                    value="Red"
                ),
                catalogue_pb2.ProductAttribute(
                    name="Size",
                    value="M"
                )
            ],
            variants=[
                catalogue_pb2.ProductVariant(
                    name="Variant 1",
                    attributes={"Color": "Red", "Size": "M"},
                    price=120.0,
                    stock=5,
                    sku="VARIANT1SKU",
                    image_url="http://example.com/variant1.jpg",
                    hash=str(uuid.uuid4())
                ),
                catalogue_pb2.ProductVariant(
                    name="Variant 2",
                    attributes={"Color": "Blue", "Size": "L"},
                    price=130.0,
                    stock=3,
                    sku="VARIANT2SKU",
                    image_url="http://example.com/variant2.jpg",
                    hash=str(uuid.uuid4())
                )
            ]
        )
        create_response = stub.CreateProduct(create_request)
        print("Created Product:")
        print_product(create_response)

        # Get the product
        get_request = catalogue_pb2.GetProductRequest(hash=create_response.hash)
        get_response = stub.GetProduct(get_request)
        print("\nRetrieved Product:")
        print_product(get_response)

        # List all products
        list_response = stub.ListProducts(empty_pb2.Empty())
        print("\nList of Products:")
        for product in list_response.products:
            print_product(product)
            print("\n")

        # Update the product
        update_request = catalogue_pb2.UpdateProductRequest(
            hash=create_response.hash,
            name="Updated Test Product",
            description="An updated product for testing",
            category_id=1,
            brand_id=1,
            base_price=150.0,
            stock=20,
            sku="TESTSKU",
            weight=0.5,
            dimensions="10x10x10",
            is_active=True,
            images=[
                catalogue_pb2.ProductImage(
                    image_url="http://example.com/image1_updated.jpg",
                    alt_text="Updated Image 1",
                    is_primary=True
                ),
                catalogue_pb2.ProductImage(
                    image_url="http://example.com/image2_updated.jpg",
                    alt_text="Updated Image 2",
                    is_primary=False
                )
            ],
            attributes=[
                catalogue_pb2.ProductAttribute(
                    name="Color",
                    value="Blue"
                ),
                catalogue_pb2.ProductAttribute(
                    name="Size",
                    value="L"
                )
            ],
            variants=[
                catalogue_pb2.ProductVariant(
                    name="Updated Variant 1",
                    attributes={"Color": "Blue", "Size": "L"},
                    price=140.0,
                    stock=8,
                    sku="UPDATEDVARIANT1SKU",
                    image_url="http://example.com/updated_variant1.jpg",
                    hash=str(uuid.uuid4())
                ),
                catalogue_pb2.ProductVariant(
                    name="Updated Variant 2",
                    attributes={"Color": "Green", "Size": "XL"},
                    price=160.0,
                    stock=6,
                    sku="UPDATEDVARIANT2SKU",
                    image_url="http://example.com/updated_variant2.jpg",
                    hash=str(uuid.uuid4())
                )
            ]
        )
        update_response = stub.UpdateProduct(update_request)
        print("Updated Product:")
        print_product(update_response)

        # Delete the product
        delete_request = catalogue_pb2.DeleteProductRequest(hash=create_response.hash)
        stub.DeleteProduct(delete_request)
        print("\nDeleted Product")

if __name__ == '__main__':
    run()
