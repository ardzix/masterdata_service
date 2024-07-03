# admin.py
from django.contrib import admin
from catalogue.models import Category, Brand, Product, ProductVariant, ProductImage, ProductAttribute

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'base_price', 'stock', 'is_active', 'hash')
    inlines = [ProductImageInline, ProductAttributeInline, ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'price', 'stock', 'hash')

admin.site.register(Category)
admin.site.register(Brand)
