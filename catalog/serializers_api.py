''' Serialiser '''
from django.conf import settings
from rest_framework import serializers

from .models import Brand, Product, ProductVariant


class BrandSerializers(serializers.ModelSerializer):
    '''
    Brand Serializers
    '''
    class Meta:
        ''' Meta information serializer'''
        model = Brand
        fields = ('name', 'id')


class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        ''' Meta information serializer'''
        model = ProductVariant
        fields = ('id', 'product', 'name', 'description', 'image', 'notes', 'is_active', 'pack', 'size')


class ProductSerializers(serializers.ModelSerializer):
    '''
    Product Serializers
    '''
    product_variant = ProductVariantSerializer(many=True, read_only=True)
    class Meta:
        ''' Meta information serializer'''
        model = Product
        fields = ('image', 'pack', 'size', 'name', 'id', 'brand', 'product_variant')
