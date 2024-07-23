# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: catalogue.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x63\x61talogue.proto\x12\tcatalogue\"!\n\x11GetProductRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\"\xdc\x02\n\x14\x43reateProductRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x13\n\x0b\x63\x61tegory_id\x18\x03 \x01(\x05\x12\x10\n\x08\x62rand_id\x18\x04 \x01(\x05\x12\x12\n\nbase_price\x18\x05 \x01(\x01\x12\r\n\x05stock\x18\x06 \x01(\x05\x12\x0b\n\x03sku\x18\x07 \x01(\t\x12\x0e\n\x06weight\x18\x08 \x01(\x01\x12\x12\n\ndimensions\x18\t \x01(\t\x12\x11\n\tis_active\x18\n \x01(\x08\x12\x0c\n\x04hash\x18\x0b \x01(\t\x12\'\n\x06images\x18\x0c \x03(\x0b\x32\x17.catalogue.ProductImage\x12/\n\nattributes\x18\r \x03(\x0b\x32\x1b.catalogue.ProductAttribute\x12+\n\x08variants\x18\x0e \x03(\x0b\x32\x19.catalogue.ProductVariant\"\xdc\x02\n\x14UpdateProductRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x13\n\x0b\x63\x61tegory_id\x18\x04 \x01(\x05\x12\x10\n\x08\x62rand_id\x18\x05 \x01(\x05\x12\x12\n\nbase_price\x18\x06 \x01(\x01\x12\r\n\x05stock\x18\x07 \x01(\x05\x12\x0b\n\x03sku\x18\x08 \x01(\t\x12\x0e\n\x06weight\x18\t \x01(\x01\x12\x12\n\ndimensions\x18\n \x01(\t\x12\x11\n\tis_active\x18\x0b \x01(\x08\x12\'\n\x06images\x18\x0c \x03(\x0b\x32\x17.catalogue.ProductImage\x12/\n\nattributes\x18\r \x03(\x0b\x32\x1b.catalogue.ProductAttribute\x12+\n\x08variants\x18\x0e \x03(\x0b\x32\x19.catalogue.ProductVariant\"$\n\x14\x44\x65leteProductRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\"G\n\x0cProductImage\x12\x11\n\timage_url\x18\x01 \x01(\t\x12\x10\n\x08\x61lt_text\x18\x02 \x01(\t\x12\x12\n\nis_primary\x18\x03 \x01(\x08\"/\n\x10ProductAttribute\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\xdc\x01\n\x0eProductVariant\x12\x0c\n\x04name\x18\x01 \x01(\t\x12=\n\nattributes\x18\x02 \x03(\x0b\x32).catalogue.ProductVariant.AttributesEntry\x12\r\n\x05price\x18\x03 \x01(\x01\x12\r\n\x05stock\x18\x04 \x01(\x05\x12\x0b\n\x03sku\x18\x05 \x01(\t\x12\x11\n\timage_url\x18\x06 \x01(\t\x12\x0c\n\x04hash\x18\x07 \x01(\t\x1a\x31\n\x0f\x41ttributesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xd7\x02\n\x0fProductResponse\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x13\n\x0b\x63\x61tegory_id\x18\x04 \x01(\x05\x12\x10\n\x08\x62rand_id\x18\x05 \x01(\x05\x12\x12\n\nbase_price\x18\x06 \x01(\x01\x12\r\n\x05stock\x18\x07 \x01(\x05\x12\x0b\n\x03sku\x18\x08 \x01(\t\x12\x0e\n\x06weight\x18\t \x01(\x01\x12\x12\n\ndimensions\x18\n \x01(\t\x12\x11\n\tis_active\x18\x0b \x01(\x08\x12\'\n\x06images\x18\x0c \x03(\x0b\x32\x17.catalogue.ProductImage\x12/\n\nattributes\x18\r \x03(\x0b\x32\x1b.catalogue.ProductAttribute\x12+\n\x08variants\x18\x0e \x03(\x0b\x32\x19.catalogue.ProductVariant\"D\n\x14ListProductsResponse\x12,\n\x08products\x18\x01 \x03(\x0b\x32\x1a.catalogue.ProductResponse\"\"\n\x12GetCategoryRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\"O\n\x15\x43reateCategoryRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x13\n\x0bparent_hash\x18\x03 \x01(\t\"]\n\x15UpdateCategoryRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x13\n\x0bparent_hash\x18\x04 \x01(\t\"%\n\x15\x44\x65leteCategoryRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\"X\n\x10\x43\x61tegoryResponse\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x13\n\x0bparent_hash\x18\x04 \x01(\t\"I\n\x16ListCategoriesResponse\x12/\n\ncategories\x18\x01 \x03(\x0b\x32\x1b.catalogue.CategoryResponse\"\x07\n\x05\x45mpty2\xf7\x05\n\x10\x43\x61talogueService\x12\x46\n\nGetProduct\x12\x1c.catalogue.GetProductRequest\x1a\x1a.catalogue.ProductResponse\x12L\n\rCreateProduct\x12\x1f.catalogue.CreateProductRequest\x1a\x1a.catalogue.ProductResponse\x12L\n\rUpdateProduct\x12\x1f.catalogue.UpdateProductRequest\x1a\x1a.catalogue.ProductResponse\x12\x42\n\rDeleteProduct\x12\x1f.catalogue.DeleteProductRequest\x1a\x10.catalogue.Empty\x12\x41\n\x0cListProducts\x12\x10.catalogue.Empty\x1a\x1f.catalogue.ListProductsResponse\x12I\n\x0bGetCategory\x12\x1d.catalogue.GetCategoryRequest\x1a\x1b.catalogue.CategoryResponse\x12O\n\x0e\x43reateCategory\x12 .catalogue.CreateCategoryRequest\x1a\x1b.catalogue.CategoryResponse\x12O\n\x0eUpdateCategory\x12 .catalogue.UpdateCategoryRequest\x1a\x1b.catalogue.CategoryResponse\x12\x44\n\x0e\x44\x65leteCategory\x12 .catalogue.DeleteCategoryRequest\x1a\x10.catalogue.Empty\x12\x45\n\x0eListCategories\x12\x10.catalogue.Empty\x1a!.catalogue.ListCategoriesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'catalogue_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRODUCTVARIANT_ATTRIBUTESENTRY']._loaded_options = None
  _globals['_PRODUCTVARIANT_ATTRIBUTESENTRY']._serialized_options = b'8\001'
  _globals['_GETPRODUCTREQUEST']._serialized_start=30
  _globals['_GETPRODUCTREQUEST']._serialized_end=63
  _globals['_CREATEPRODUCTREQUEST']._serialized_start=66
  _globals['_CREATEPRODUCTREQUEST']._serialized_end=414
  _globals['_UPDATEPRODUCTREQUEST']._serialized_start=417
  _globals['_UPDATEPRODUCTREQUEST']._serialized_end=765
  _globals['_DELETEPRODUCTREQUEST']._serialized_start=767
  _globals['_DELETEPRODUCTREQUEST']._serialized_end=803
  _globals['_PRODUCTIMAGE']._serialized_start=805
  _globals['_PRODUCTIMAGE']._serialized_end=876
  _globals['_PRODUCTATTRIBUTE']._serialized_start=878
  _globals['_PRODUCTATTRIBUTE']._serialized_end=925
  _globals['_PRODUCTVARIANT']._serialized_start=928
  _globals['_PRODUCTVARIANT']._serialized_end=1148
  _globals['_PRODUCTVARIANT_ATTRIBUTESENTRY']._serialized_start=1099
  _globals['_PRODUCTVARIANT_ATTRIBUTESENTRY']._serialized_end=1148
  _globals['_PRODUCTRESPONSE']._serialized_start=1151
  _globals['_PRODUCTRESPONSE']._serialized_end=1494
  _globals['_LISTPRODUCTSRESPONSE']._serialized_start=1496
  _globals['_LISTPRODUCTSRESPONSE']._serialized_end=1564
  _globals['_GETCATEGORYREQUEST']._serialized_start=1566
  _globals['_GETCATEGORYREQUEST']._serialized_end=1600
  _globals['_CREATECATEGORYREQUEST']._serialized_start=1602
  _globals['_CREATECATEGORYREQUEST']._serialized_end=1681
  _globals['_UPDATECATEGORYREQUEST']._serialized_start=1683
  _globals['_UPDATECATEGORYREQUEST']._serialized_end=1776
  _globals['_DELETECATEGORYREQUEST']._serialized_start=1778
  _globals['_DELETECATEGORYREQUEST']._serialized_end=1815
  _globals['_CATEGORYRESPONSE']._serialized_start=1817
  _globals['_CATEGORYRESPONSE']._serialized_end=1905
  _globals['_LISTCATEGORIESRESPONSE']._serialized_start=1907
  _globals['_LISTCATEGORIESRESPONSE']._serialized_end=1980
  _globals['_EMPTY']._serialized_start=1982
  _globals['_EMPTY']._serialized_end=1989
  _globals['_CATALOGUESERVICE']._serialized_start=1992
  _globals['_CATALOGUESERVICE']._serialized_end=2751
# @@protoc_insertion_point(module_scope)