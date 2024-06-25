# grpc_services.py
import grpc
from django.core.exceptions import ObjectDoesNotExist
from google.protobuf import empty_pb2
from catalogue.models import Product, ProductImage, ProductVariant, ProductAttribute
from catalogue.serializers import ProductSerializer
from proto import masterdata_pb2, masterdata_pb2_grpc

class ProductService(masterdata_pb2_grpc.MasterDataServiceServicer):
    def _get_request_data(self, request):
        return {
            "name": request.name,
            "description": request.description,
            "category_id": request.category_id,
            "brand_id": request.brand_id,
            "base_price": request.base_price,
            "stock": request.stock,
            "sku": request.sku,
            "weight": request.weight,
            "dimensions": request.dimensions,
            "is_active": request.is_active,
        }

    def _get_product_response(self, product):
        images = ProductImage.objects.filter(product=product)
        image_list = [
            masterdata_pb2.ProductImage(
                image_url=image.image.url,
                alt_text=image.alt_text,
                is_primary=image.is_primary
            )
            for image in images
        ]

        attributes = ProductAttribute.objects.filter(product=product)
        attribute_list = [
            masterdata_pb2.ProductAttribute(
                name=attribute.name,
                value=attribute.value
            )
            for attribute in attributes
        ]

        variants = ProductVariant.objects.filter(product=product)
        variant_list = [
            masterdata_pb2.ProductVariant(
                name=variant.name,
                attributes=dict(variant.attributes),
                price=variant.price,
                stock=variant.stock,
                sku=variant.sku,
                image_url=variant.image.url if variant.image else ""
            )
            for variant in variants
        ]

        return masterdata_pb2.ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            category_id=product.category.id if product.category else 0,
            brand_id=product.brand.id if product.brand else 0,
            base_price=product.base_price,
            stock=product.stock,
            sku=product.sku,
            weight=product.weight,
            dimensions=product.dimensions,
            is_active=product.is_active,
            images=image_list,
            attributes=attribute_list,
            variants=variant_list
        )

    def GetProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
            return self._get_product_response(product)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

    def CreateProduct(self, request, context):
        data = self._get_request_data(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            
            # Save images
            for image in request.images:
                ProductImage.objects.create(
                    product=product,
                    image=image.image_url,
                    alt_text=image.alt_text,
                    is_primary=image.is_primary
                )
            
            # Save attributes
            for attribute in request.attributes:
                ProductAttribute.objects.create(
                    product=product,
                    name=attribute.name,
                    value=attribute.value
                )
            
            # Save variants
            for variant in request.variants:
                ProductVariant.objects.create(
                    product=product,
                    name=variant.name,
                    attributes=dict(variant.attributes),
                    price=variant.price,
                    stock=variant.stock,
                    sku=variant.sku,
                    image=variant.image_url
                )
            
            return self._get_product_response(product)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))

    def UpdateProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
            data = self._get_request_data(request)
            serializer = ProductSerializer(product, data=data, partial=True)
            if serializer.is_valid():
                product = serializer.save()
                
                # Clear existing images, attributes, and variants
                ProductImage.objects.filter(product=product).delete()
                ProductAttribute.objects.filter(product=product).delete()
                ProductVariant.objects.filter(product=product).delete()

                # Save new images
                for image in request.images:
                    ProductImage.objects.create(
                        product=product,
                        image=image.image_url,
                        alt_text=image.alt_text,
                        is_primary=image.is_primary
                    )

                # Save new attributes
                for attribute in request.attributes:
                    ProductAttribute.objects.create(
                        product=product,
                        name=attribute.name,
                        value=attribute.value
                    )

                # Save new variants
                for variant in request.variants:
                    ProductVariant.objects.create(
                        product=product,
                        name=variant.name,
                        attributes=dict(variant.attributes),
                        price=variant.price,
                        stock=variant.stock,
                        sku=variant.sku,
                        image=variant.image_url
                    )
                
                return self._get_product_response(product)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

    def DeleteProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
            product.delete()
            return empty_pb2.Empty()
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

    def ListProducts(self, request, context):
        products = Product.objects.all()
        response = masterdata_pb2.ListProductsResponse()
        for product in products:
            response.products.append(self._get_product_response(product))
        return response
