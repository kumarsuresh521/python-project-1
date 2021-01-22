import base64
from collections import OrderedDict

import boto3
from django.conf import settings
from django.db import models
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .constants import ADMIN_PAGE_SIZE


class CustomPagination(PageNumberPagination):
    page_size = ADMIN_PAGE_SIZE
    page_size_query_param = 'limit'
    def get_paginated_response(self, data):
        next_page = int(self.page.number) + 1 if self.page.has_next() else None
        previous_page = int(self.page.number) - 1 if self.page.has_previous() else None
        return Response(OrderedDict([
            ('next', next_page),
            ('previous', previous_page),
            ('total_count', self.page.paginator.count),
            ('results', data)
        ]))


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

def upload_image(image_obj, file_name):
    connection_kwargs = {
        "region_name": settings.S3DIRECT_REGION,
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY
    }
    content_type = 'image/jpeg'
    params = {
        "ACL": "public-read",
        'Key': file_name
    }

    s3_obj = boto3.resource("s3", **connection_kwargs)
    bucket = s3_obj.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Body=base64.b64decode(image_obj), **params)
    return True
