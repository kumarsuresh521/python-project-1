'''
Catalog Models
'''

from django.db import models
from example.core.helper import TimestampModel
from app.models import User
from .message import UNIQUE_BRAND_NAME, UNIQUE_PRODUCT_NAME

class Brand(TimestampModel):
    '''
    Brand Model
    '''
    name = models.CharField(max_length=254, unique=True, error_messages={'unique': UNIQUE_BRAND_NAME})
    mobile_number = models.CharField('Mobile Number', max_length=20, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    image = models.CharField(max_length=254, null=True, blank=True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brand_supplier')
    address1 = models.CharField('Address Line 1', max_length=150)
    address2 = models.CharField('Address Line 2', max_length=150, null=True, blank=True)
    town = models.CharField('Town', max_length=150)
    postcode = models.CharField('Postcode', max_length=15)
    country_id = models.PositiveIntegerField('country_id')
    country_name = models.CharField('country_name', max_length=50)
    county_id = models.PositiveIntegerField('county_id')
    county_name = models.CharField('county_name', max_length=50)

    class Meta:
        ordering = ['name',]

class Product(TimestampModel):
    '''
    Products model
    '''
    name = models.CharField(max_length=254, unique=True, error_messages={'unique': UNIQUE_PRODUCT_NAME})
    image = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=254, null=True, blank=True)
    pack = models.CharField(max_length=254, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_product')
    admin_notes = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['name',]

class ProductVariant(TimestampModel):
    '''
    Product variant model
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant')
    name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=254, null=True, blank=True)
    size = models.CharField(max_length=254, null=True, blank=True)
    pack = models.CharField(max_length=254, null=True, blank=True)
    notes = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['name',]

class Contact(TimestampModel):
    brand = models.ForeignKey(Brand, related_name='brand_contact')
    name = models.CharField(max_length=30)
    job_title = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['name',]