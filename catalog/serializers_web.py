''' Serialiser '''
import uuid
from django.conf import settings
from example.core.helper import upload_image
from rest_framework import serializers
from django.forms import ValidationError
from .message import UNIQUE_PRODUCT_VARIANT_NAME, UNIQUE_CONTACT_EMAIL
from django.db.models import Q
from .models import Brand, Product, Contact, ProductVariant


class BrandSerializers(serializers.ModelSerializer):
    '''
    Brand Serializers
    '''
    class Meta:
        ''' Meta information serializer'''
        model = Brand
        fields = ('id', 'name', 'image', 'supplier',
                  'mobile_number', 'notes', 'address1', 'address2', 'town', 'postcode',
                  'country_id', 'country_name', 'county_id', 'county_name', 'is_active')

    def __init__(self, *args, **kwargs):
        super(BrandSerializers, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

            image_obj = self.request.data.get('image', '')
            if image_obj:
                image_name = '%s/%s.jpeg' % (settings.AWS_STORE_CAMPAIGN_PATH, uuid.uuid4())
                self.request.data['image'] = image_name
                upload_image(image_obj, image_name)

    def create(self, validated_data):
        validated_data['is_active'] = True
        instance = super(BrandSerializers, self).create(validated_data)
        return instance
    
    def update(self, instance, validated_data):
        instance = super(BrandSerializers, self).update(instance, validated_data)
        return instance


class ProductVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    class Meta:
        ''' Meta information serializer'''
        model = ProductVariant
        fields = ('id', 'product', 'name', 'description', 'image', 'notes', 'is_active', 'pack', 'size', 'product_name')

    def __init__(self, *args, **kwargs):
        super(ProductVariantSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

            image_obj = self.request.data.get('image', '')
            if image_obj:
                image_name = '%s/%s.jpeg' % (settings.AWS_STORE_CAMPAIGN_PATH, uuid.uuid4())
                self.request.data['image'] = image_name
                upload_image(image_obj, image_name)

    def validate_name(self, data):
        try:
            ProductVariant.objects.get(name__iexact=data, product_id=self.request.data.get('product'))
            raise ValidationError(UNIQUE_PRODUCT_VARIANT_NAME)
        except ProductVariant.DoesNotExist:
            return data

    def create(self, validated_data):
        return super(ProductVariantSerializer, self).create(validated_data)

    def get_product_name(self, obj):
        _ = self.__class__.__name__
        return obj.product.name


class ProductSerializer(serializers.ModelSerializer):
    '''
    Product Serializers
    '''
    product_variant = serializers.SerializerMethodField(read_only=True)
    variant = serializers.SerializerMethodField()
    class Meta:
        ''' Meta information serializer'''
        model = Product
        fields = ('id', 'name', 'image', 'description', 'size', 'pack', 'brand', 'is_active', 'admin_notes', 'variant', 'product_variant')

    def get_variant(self, obj):
        _ = self.__class__.__name__
        return obj.product_variant.count()

    def get_product_variant(self, obj):
        product_variants = obj.product_variant.filter(is_active=True)
        data = ProductVariantSerializer(product_variants, many=True).data
        return data

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

            image_obj = self.request.data.get('image', '')
            if image_obj:
                image_name = '%s/%s.jpeg' % (settings.AWS_STORE_CAMPAIGN_PATH, uuid.uuid4())
                self.request.data['image'] = image_name
                upload_image(image_obj, image_name)

    def create(self, validated_data):
        return super(ProductSerializer, self).create(validated_data)



class BrandProductsSerializers(serializers.ModelSerializer):
    '''
    Brand Serializers
    '''
    products = serializers.SerializerMethodField()
    class Meta:
        ''' Meta information serializer'''
        model = Brand
        fields = ('id', 'name', 'image', 'products', 'is_active')

    def get_products(self, obj):
        _ = self.__class__.__name__
        products = Product.objects.filter(brand_id=obj.id)
        return ProductSerializer(products, many=True).data

class BrandContactSerializer(serializers.ModelSerializer):

    class Meta:
        ''' Meta information serializer'''
        model = Contact
        fields = ('id', 'brand', 'name', 'job_title', 'mobile_number', 'notes', 'email', 'is_active')

    def validate_email(self, data):
        if data:
            try:
                if 'contact_id' in self.context:
                    Contact.objects.get(Q(email__iexact=data.lower()) & Q(brand_id=self.get_initial().get('brand')) & ~Q(id__in=[self.context['contact_id']]))
                else:
                    Contact.objects.get(Q(email__iexact=data.lower()) & Q(brand_id=self.get_initial().get('brand')))
                raise ValidationError(UNIQUE_CONTACT_EMAIL)
            except Contact.DoesNotExist:
                return data
        return data
