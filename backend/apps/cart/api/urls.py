from django.urls import path

from .views import (
    CartAPIView,
    CartItemAPIView,
    CartItemDetailAPIView,
)

urlpatterns = [

    path(
        "",
        CartAPIView.as_view(),
        name="cart",
    ),

    path(
        "items/",
        CartItemAPIView.as_view(),
        name="cart-items",
    ),

    path(
        "items/<uuid:item_id>/",
        CartItemDetailAPIView.as_view(),
        name="cart-item-detail",
    ),
]