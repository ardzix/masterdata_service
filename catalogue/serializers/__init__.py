from rest_framework import serializers
from ..models import Category, Brand, Product, ProductVariant, ProductImage, ProductAttribute

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    product_attributes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    variants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category_hash = serializers.CharField(allow_blank=False)
    brand_hash = serializers.CharField(allow_blank=False)

    def validate(self, data):
        validated_data = super().validate(data)
        category = Category.objects.filter(hash=validated_data.pop('category_hash')).first()
        validated_data['category'] = category
        brand = Brand.objects.filter(hash=validated_data.pop('brand_hash')).first()
        validated_data['brand'] = brand
        return validated_data

    class Meta:
        model = Product
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'
