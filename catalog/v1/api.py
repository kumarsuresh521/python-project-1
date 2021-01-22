'''
Api requests for catalog module
'''
from catalog.models import Brand, Product
from collections import OrderedDict
from catalog.serializers_api import BrandSerializers, ProductSerializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from example.core.constants import *
from example.core.helper import CustomPagination
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


class ListBrandView(generics.ListAPIView):
    '''
    Brand list api 
    '''
    serializer_class = BrandSerializers
    pagination_class = CustomPagination

    def get_queryset(self):
        try:
            brand_ids = json.loads(self.request.GET.get('brand_ids'))
            return Brand.objects.filter(id__in=brand_ids)
        except (KeyError, ValueError, AttributeError):
            return Brand.objects.filter(is_active=True)

class MediaAssetsProductView(APIView):
    '''
    API to return product object using product product_ids
    request format
    "product_ids": [
            1,
            2
        ],
    {"product_ids": [
        {
            "product_id": 1
        },
        {
            "product_id": 2
        }
    ]}
    '''

    def post(self, *args, **kwargs):
        response_obj = {}
        product_ids = self.request.data.get('product_ids')
        product_list = Product.objects.filter(id__in=product_ids)
        product_serializer = ProductSerializers(product_list, many=True)
        response = product_serializer.data
        
        if response:
            response_obj['results'] = response
            status = HTTP_SUCCESS
        else:
            response_obj['message'] = 'No record found'
            status = HTTP_API_ERROR

        return Response(response_obj, status=status)


class ListBrandIdsView(APIView):
    def post(self, *args, **kwargs):
        response_obj = {}
        brand_ids = self.request.data.get('brand_ids')
        brand_list = Brand.objects.filter(id__in=brand_ids).order_by('name')
        brand_serializer = BrandSerializers(brand_list, many=True)
        response = brand_serializer.data

        if response:
            response_obj['results'] = response
            status = HTTP_SUCCESS
        else:
            response_obj['message'] = 'No record found'
            status = HTTP_API_ERROR

        return Response(response_obj, status=status)