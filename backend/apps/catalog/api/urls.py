
from django.urls import path

from .views import (
    CategoryAPIView,
    ProductAPIView,
    ProductVariantAPIView
)

urlpatterns = [
    path(
        "categories/",
        CategoryAPIView.as_view(),
        name="category-api",
    ),
    path(
    "<uuid:vendor_id>/products/",
    ProductAPIView.as_view(),
    name="vendor-products",
),
path(
    "products/<uuid:product_id>/variants/",
    ProductVariantAPIView.as_view(),
    name="product-variants",
),
]