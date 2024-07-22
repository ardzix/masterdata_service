# grpc_services.py
import grpc
import uuid
from django.core.exceptions import ObjectDoesNotExist
from google.protobuf import empty_pb2
from catalogue.models import Product, ProductImage, ProductVariant, ProductAttribute, Category
from catalogue.serializers import ProductSerializer, CategorySerializer
from . import catalogue_pb2, catalogue_pb2_grpc

class ProductService(catalogue_pb2_grpc.CatalogueServiceServicer):
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
            "hash": request.hash if request.hash else None,
        }

    def _get_product_response(self, product):
        images = ProductImage.objects.filter(product=product)
        image_list = [
            catalogue_pb2.ProductImage(
                image_url=image.image.url,
                alt_text=image.alt_text,
                is_primary=image.is_primary
            )
            for image in images
        ]

        attributes = ProductAttribute.objects.filter(product=product)
        attribute_list = [
            catalogue_pb2.ProductAttribute(
                name=attribute.name,
                value=attribute.value
            )
            for attribute in attributes
        ]

        variants = ProductVariant.objects.filter(product=product)
        variant_list = [
            catalogue_pb2.ProductVariant(
                name=variant.name,
                attributes=dict(variant.attributes),
                price=variant.price,
                stock=variant.stock,
                sku=variant.sku,
                image_url=variant.image.url if variant.image else "",
                hash=str(variant.hash)
            )
            for variant in variants
        ]

        return catalogue_pb2.ProductResponse(
            hash=str(product.hash),
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
            product = Product.objects.get(hash=request.hash)
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
                    image=variant.image_url,
                    hash=variant.hash if variant.hash else uuid.uuid4()
                )
            
            return self._get_product_response(product)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))

    def UpdateProduct(self, request, context):
        try:
            product = Product.objects.get(hash=request.hash)
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
                        image=variant.image_url,
                        hash=variant.hash if variant.hash else uuid.uuid4()
                    )
                
                return self._get_product_response(product)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

    def DeleteProduct(self, request, context):
        try:
            product = Product.objects.get(hash=request.hash)
            product.delete()
            return empty_pb2.Empty()
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")

    def ListProducts(self, request, context):
        products = Product.objects.all()
        response = catalogue_pb2.ListProductsResponse()
        for product in products:
            response.products.append(self._get_product_response(product))
        return response


    # Category related methods
    def GetCategory(self, request, context):
        try:
            category = Category.objects.get(hash=request.hash)
            return self._get_category_response(category)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

    def CreateCategory(self, request, context):
        parent = Category.objects.get(hash=request.parent_hash) if request.parent_hash else None
        data = {
            "name": request.name,
            "description": request.description,
            "parent": parent,
            "hash": str(uuid.uuid4())
        }
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            category = serializer.save()
            return self._get_category_response(category)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))

    def UpdateCategory(self, request, context):
        try:
            category = Category.objects.get(hash=request.hash)
            parent = Category.objects.get(hash=request.parent_hash) if request.parent_hash else None
            data = {
                "name": request.name,
                "description": request.description,
                "parent": parent
            }
            serializer = CategorySerializer(category, data=data, partial=True)
            if serializer.is_valid():
                category = serializer.save()
                return self._get_category_response(category)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

    def DeleteCategory(self, request, context):
        try:
            category = Category.objects.get(hash=request.hash)
            category.delete()
            return empty_pb2.Empty()
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

    def ListCategories(self, request, context):
        categories = Category.objects.all()
        response = catalogue_pb2.ListCategoriesResponse()
        for category in categories:
            response.categories.append(self._get_category_response(category))
        return response

    def _get_category_response(self, category):
        parent_hash = category.parent.hash if category.parent else ""
        return catalogue_pb2.CategoryResponse(
            hash=str(category.hash),
            name=category.name,
            description=category.description,
            parent_hash=parent_hash
        )