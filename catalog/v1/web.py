'''
Api requests for catalog module
'''

import json
from collections import OrderedDict
from django.db.models import Case, Count, FloatField, Q, Sum, Value, When, F
from catalog.models import Brand, Product, Contact, ProductVariant
from catalog.serializers_web import (BrandProductsSerializers, ProductVariantSerializer,
                                     BrandSerializers, ProductSerializer, BrandContactSerializer)
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.http import Http404
from example.core import constants
from example.core.helper import CustomPagination
from rest_framework import filters, generics, exceptions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from ..filters import ProductVariantFilter

from ..message import *


class ListBrandView(generics.ListAPIView):
    '''
    Brand list api 
    '''
    serializer_class = BrandSerializers
    pagination_class = CustomPagination

    def get_queryset(self):
        _ = self.__class__.__name__
        return Brand.objects.filter(is_active=True).order_by('name')


class ListSupplierBrandView(generics.ListAPIView):
    '''
    Brand list api 
    '''
    serializer_class = BrandSerializers
    pagination_class = CustomPagination

    def get_queryset(self):
        return Brand.objects.filter(supplier=self.kwargs['supplier_id']).order_by('name')

class CampaignSupplierBrandView(generics.ListAPIView):
    '''
    Brand list api 
    '''
    serializer_class = BrandSerializers

    def get_queryset(self):
        return Brand.objects.filter(is_active=True, supplier=self.kwargs['supplier_id']).order_by('name')


class CreateBrandView(generics.CreateAPIView):
    '''
    Brand create api 
    '''
    serializer_class = BrandSerializers


class UpdateBrandView(generics.RetrieveUpdateAPIView):
    '''
    Brand Update api 
    '''
    serializer_class = BrandSerializers
    def get_object(self):
        try:
            obj = Brand.objects.get(id=self.kwargs.get('brand_id'))
        except Brand.DoesNotExist:
            raise exceptions.APIException(DOES_NOT_EXIST.format("Brand"))
        return obj

    def retrieve(self, *args, **kwargs):
        '''Retrieve'''
        try:
            return super(UpdateBrandView, self).retrieve(*args, **kwargs)
        except (Http404, Brand.DoesNotExist):
            return Response({MESSAGE: BRAND_NOT_FOUND}, status=HTTP_API_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            return super(UpdateBrandView,self).patch(request, *args, **kwargs)
        except Brand.DoesNotExist:
            return Response({MESSAGE: BRAND_NOT_FOUND}, status=HTTP_API_ERROR)
        return Response()


class DeleteBrandView(generics.DestroyAPIView):
    '''
    Brand Delete api 
    '''
    serializer_class = BrandSerializers
    def get_object(self):
        return Brand.objects.get(id=self.kwargs['id'])


class BrandDetailView(generics.RetrieveAPIView):
    '''
    Get Brand Detail
    '''
    serializer_class = BrandSerializers

    def get_object(self):
        return Brand.objects.get(id=self.kwargs['pk'])


class ProductView(generics.ListCreateAPIView):
    '''
    Product View api 
    '''
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Product.objects.filter(brand_id=self.kwargs['brand_id']).order_by('name')


class ProductManageView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Product View api 
    '''
    serializer_class = ProductSerializer

    def get_object(self):
        return Product.objects.get(pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            object.is_active = False
            object.save()
            return Response({'success': REQUEST_SUCCESSFULL})
        except Product.DoesNotExist:
            return Response({"message": PRODUCT_NOT_FOUND}, status=HTTP_API_ERROR)

    def retrieve(self, *args, **kwargs):
        '''Retrieve'''
        try:
            return super(ProductManageView, self).retrieve(*args, **kwargs)
        except (Http404, Product.DoesNotExist):
            return Response({MESSAGE: PRODUCT_NOT_FOUND}, status=HTTP_API_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            if 'is_active' in self.request.data:
                object.product_variant.update(is_active=self.request.data.get('is_active'))
            return super(ProductManageView,self).patch(request, *args, **kwargs)
        except (Http404, Product.DoesNotExist):
            return Response({MESSAGE: PRODUCT_NOT_FOUND}, status=HTTP_API_ERROR)


class ProductVariantView(generics.ListCreateAPIView):
    '''
    Product Variant View api 
    '''
    queryset = ProductVariant.objects.all().order_by('name')
    serializer_class = ProductVariantSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductVariantFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset.filter(product__brand=self.kwargs.get('brand_id')).order_by('name')

class ProductVariantManageView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Product Variant View api 
    '''
    serializer_class = ProductVariantSerializer

    def get_object(self):
        return ProductVariant.objects.get(pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            object.is_active = False
            object.save()
            return Response({'success': REQUEST_SUCCESSFULL})
        except ProductVariant.DoesNotExist:
            return Response({"message": PRODUCT_NOT_FOUND}, status=HTTP_API_ERROR)

    def retrieve(self, *args, **kwargs):
        '''Retrieve'''
        try:
            return super(ProductVariantManageView, self).retrieve(*args, **kwargs)
        except (Http404, ProductVariant.DoesNotExist):
            return Response({MESSAGE: PRODUCT_NOT_FOUND}, status=HTTP_API_ERROR)


class BrandProductsView(generics.ListAPIView):
    serializer_class = BrandProductsSerializers
    pagination_class = CustomPagination
    def get_queryset(self):
        try:
            brand_ids = self.request.GET.get('brands').split(',')
            return Brand.objects.filter(id__in=brand_ids).order_by('name')
        except (KeyError, ValueError, AttributeError):
            return Brand.objects.filter(is_active=True).order_by('name')


class BrandListDetailView(generics.ListAPIView):
    serializer_class = BrandSerializers
    def get_queryset(self):
        try:
            brand_ids = self.request.GET.get('brands').split(',')
            return Brand.objects.filter(is_active=True, id__in=brand_ids).order_by('name')
        except (KeyError, ValueError, AttributeError):
            return Brand.objects.filter(is_active=True).order_by('name')


class ListBrandsProductView(generics.ListAPIView):
    '''
    List Brands Product View
    '''
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        if self.request.GET.get('brands'):
            brands = self.request.GET.get('brands').split(',')
            product_list = Product.objects.filter(is_active=True, brand_id__in=brands).order_by('name')
            if self.request.GET.get('search'):
               product_list = product_list.filter(Q(name__icontains=self.request.GET.get('search')) | Q(product_variant__name__icontains=self.request.GET.get('search')))
            return product_list
        return Product.objects.filter(is_active=True).order_by('name')


class ListCampaignProductView(generics.ListAPIView):
    '''
    Product list api 
    '''
    serializer_class = ProductSerializer
    def get_queryset(self):
        if self.request.GET.get('product_ids'):
            product_ids = self.request.GET.get('product_ids').split(',')
            return Product.objects.filter(is_active=True, id__in=product_ids).order_by('name')
        return Product.objects.filter(is_active=True).order_by('name')

class SupplierBrandCountView(generics.RetrieveAPIView):
    '''
    API for calculating brand count for a supplier
    '''

    def get(self, request, *args, **kwargs):
        ids = json.loads(self.request.GET.get('supplier_ids'))
        brand_count_arr=[]
        for supplier_id in ids:
            obj_count = Brand.objects.filter(is_active=True, supplier=supplier_id).count()
            stats={'brand_count':obj_count, 'supplier_id':supplier_id}
            brand_count_arr.append(stats)
        return Response(brand_count_arr)

class BrandStatsView(generics.ListAPIView):
    '''
    API for calculating brand count for a supplier
    '''

    def get(self, request, *args, **kwargs):
        brand_ids = json.loads(self.request.GET.get('brand_ids'))
        brands = Brand.objects.filter(id__in=brand_ids).order_by('name')
        count_arr = []
        for brand in brands:
            product_count = brand.brand_product.all().count()
            contact_count = brand.brand_contact.all().count()
            count_ar = {
                "id": brand.id,
                "contact_count": contact_count,
                "product_count": product_count,
                "brand_id": brand.id,
            }
            count_arr.append(count_ar)
        return Response(count_arr)


class DeactivateSupplierBrandsView(generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):
        response_data = {}
        brand_query= {}
        product_query = {}

        if 'supplier_id' in self.kwargs.keys():
            supplier_id=self.kwargs.get('supplier_id')
            brand_query.update({'supplier':supplier_id})
        elif 'brand_id' in self.kwargs.keys():
            brand_id=self.kwargs.get('brand_id')
            brand_query.update({'id':brand_id})
            products=self.kwargs.get('brand_id')
            product_query.update({'brand__id':products})

        brands = Brand.objects.filter(**brand_query)
        brands.update(is_active=request.data['is_active'])
        product_query.update({'brand__in':brands})
        Product.objects.filter(**product_query).update(is_active=request.data['is_active'])
        response_data[SUCCESS] = REQUEST_SUCCESSFULL

        return Response(response_data, status=HTTP_200_SUCCESS)

class BrandContactView(generics.ListCreateAPIView):

    serializer_class = BrandContactSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Contact.objects.filter(brand__id=self.kwargs.get('brand_id')).order_by('name')

class UpdateContactView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BrandContactSerializer

    def get_object(self):
        try:
            obj = Contact.objects.get(pk=self.kwargs.get('contact_id'))
        except Contact.DoesNotExist:
            raise exceptions.APIException(DOES_NOT_EXIST.format("Contact"))
        return obj

    def get_serializer_context(self):
        context = super(UpdateContactView, self).get_serializer_context()
        context.update({'contact_id': self.kwargs['contact_id']})
        return context

    def delete(self,request, *args, **kwargs):
        super(UpdateContactView, self).delete(request, *args, **kwargs)
        return Response({'message': DELETED_SUCCESSFULL})