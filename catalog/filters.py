'''filters.py'''
import datetime
import json
import rest_framework_filters as filters
from django.db.models import Q
from django.utils import timezone

from .models import (Product, ProductVariant)


class ProductVariantFilter(filters.FilterSet):
    product = filters.NumberFilter(field_name='product__id')
    
    class Meta:
        model = ProductVariant
        fields = [
            'product'
        ]
