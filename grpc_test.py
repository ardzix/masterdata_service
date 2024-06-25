# grpc_client.py
import grpc
from google.protobuf import empty_pb2
from proto import masterdata_pb2, masterdata_pb2_grpc

def print_product(product):
    print(f"id: {product.id}")
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
        print(f"  - name: {variant.name}, attributes: {variant.attributes}, price: {variant.price}, stock: {variant.stock}, sku: {variant.sku}, image_url: {variant.image_url}")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = masterdata_pb2_grpc.MasterDataServiceStub(channel)

        # Create a new product
        create_request = masterdata_pb2.CreateProductRequest(
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
            images=[
                masterdata_pb2.ProductImage(
                    image_url="http://example.com/image1.jpg",
                    alt_text="Image 1",
                    is_primary=True
                ),
                masterdata_pb2.ProductImage(
                    image_url="http://example.com/image2.jpg",
                    alt_text="Image 2",
                    is_primary=False
                )
            ],
            attributes=[
                masterdata_pb2.ProductAttribute(
                    name="Color",
                    value="Red"
                ),
                masterdata_pb2.ProductAttribute(
                    name="Size",
                    value="M"
                )
            ],
            variants=[
                masterdata_pb2.ProductVariant(
                    name="Variant 1",
                    attributes={"Color": "Red", "Size": "M"},
                    price=120.0,
                    stock=5,
                    sku="VARIANT1SKU",
                    image_url="http://example.com/variant1.jpg"
                ),
                masterdata_pb2.ProductVariant(
                    name="Variant 2",
                    attributes={"Color": "Blue", "Size": "L"},
                    price=130.0,
                    stock=3,
                    sku="VARIANT2SKU",
                    image_url="http://example.com/variant2.jpg"
                )
            ]
        )
        create_response = stub.CreateProduct(create_request)
        print("Created Product:")
        print_product(create_response)

        # Get the product
        get_request = masterdata_pb2.GetProductRequest(id=create_response.id)
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
        update_request = masterdata_pb2.UpdateProductRequest(
            id=create_response.id,
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
                masterdata_pb2.ProductImage(
                    image_url="http://example.com/image1_updated.jpg",
                    alt_text="Updated Image 1",
                    is_primary=True
                ),
                masterdata_pb2.ProductImage(
                    image_url="http://example.com/image2_updated.jpg",
                    alt_text="Updated Image 2",
                    is_primary=False
                )
            ],
            attributes=[
                masterdata_pb2.ProductAttribute(
                    name="Color",
                    value="Blue"
                ),
                masterdata_pb2.ProductAttribute(
                    name="Size",
                    value="L"
                )
            ],
            variants=[
                masterdata_pb2.ProductVariant(
                    name="Updated Variant 1",
                    attributes={"Color": "Blue", "Size": "L"},
                    price=140.0,
                    stock=8,
                    sku="UPDATEDVARIANT1SKU",
                    image_url="http://example.com/updated_variant1.jpg"
                ),
                masterdata_pb2.ProductVariant(
                    name="Updated Variant 2",
                    attributes={"Color": "Green", "Size": "XL"},
                    price=160.0,
                    stock=6,
                    sku="UPDATEDVARIANT2SKU",
                    image_url="http://example.com/updated_variant2.jpg"
                )
            ]
        )
        update_response = stub.UpdateProduct(update_request)
        print("Updated Product:")
        print_product(update_response)

        # Delete the product
        delete_request = masterdata_pb2.DeleteProductRequest(id=create_response.id)
        stub.DeleteProduct(delete_request)
        print("\nDeleted Product")

if __name__ == '__main__':
    run()
