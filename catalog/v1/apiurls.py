'''urls configurations for rest api requests'''
from django.conf.urls import url

from .api import *

urlpatterns = [
    url(r'^mediaassets-product/$', MediaAssetsProductView.as_view(),
        name="mediaassets-product"),
    url(r'^brands/$', ListBrandView.as_view(), name="brand_list"),
    url(r'^brands-by-id/$', ListBrandIdsView.as_view(), name="brand_list_by_ids"),
]
