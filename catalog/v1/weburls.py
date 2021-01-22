'''urls configurations for rest api requests'''
from django.conf.urls import url

from .web import *

urlpatterns = [
    url(r'^supplier-brand-count/$', SupplierBrandCountView.as_view(), name="supplier_brand_count"),
    url(r'^brand-stats/$', BrandStatsView.as_view(), name="brand_product_count"),
    url(r'^brand-products/$', BrandProductsView.as_view(), name="brand_product_list"),
    url(r'^list-brand-products/$', ListBrandsProductView.as_view(), name="list_brand_product"),
    url(r'^brand-details/$', BrandListDetailView.as_view(), name="brand_list_details"),
    url(r'^brands/$', ListBrandView.as_view(), name="brand_list"),
    url(r'^supplier-brands/(?P<supplier_id>.+)/$', ListSupplierBrandView.as_view(), name="supplier_brand_list"),
    url(r'^campaign-supplier-brands/(?P<supplier_id>.+)/$', CampaignSupplierBrandView.as_view(), name="campaign_supplier_brand_list"),
    url(r'^brand/$', CreateBrandView.as_view(), name="add_brand"),
    url(r'^brand/(?P<brand_id>.+)/$', UpdateBrandView.as_view(), name="edit_brand"),
    url(r'^delete-brand/(?P<brand_id>.+)/$', DeleteBrandView.as_view(), name="delete_brand"),
    url(r'^brand/(?P<pk>.+)/$', BrandDetailView.as_view(), name="detail_brand"),
    url(r'^campaign-products/$', ListCampaignProductView.as_view(), name="campaign_product_list"),
    url(r'^deactivate-supplier-brands/(?P<supplier_id>.+)/$', DeactivateSupplierBrandsView.as_view(), name="deactivate_supplier_brand"),
    url(r'^deactivate-brands/(?P<brand_id>.+)/$', DeactivateSupplierBrandsView.as_view(), name="deactivate_supplier_brand"),
    url(r'^brand-contact/(?P<brand_id>\d+)/$', BrandContactView.as_view(), name="list_contact"),
    url(r'^brand-contact/', BrandContactView.as_view(), name="create_contact"),
    url(r'^update-delete-contact/(?P<contact_id>\d+)/$', UpdateContactView.as_view(), name="update_delete_contact"),

    url(r'^product/(?P<brand_id>\d+)/$', ProductView.as_view(), name="list_create_product"),
    url(r'^product-manage/(?P<pk>\d+)/$', ProductManageView.as_view(), name="manage_product"),
    url(r'^product-variant/(?P<brand_id>\d+)/$', ProductVariantView.as_view(), name="list_create_product_variant"),
    url(r'^product-variant-manage/(?P<pk>\d+)/$', ProductVariantManageView.as_view(), name="manage_product_variant"),
]   
