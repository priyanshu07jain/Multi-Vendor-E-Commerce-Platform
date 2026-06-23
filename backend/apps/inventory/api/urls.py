from django.urls import path

from .views import (
    InventoryAPIView,
    StockInAPIView,
    InventoryTransactionAPIView,
)

urlpatterns = [

    path(
        "variants/<uuid:variant_id>/inventory/",
        InventoryAPIView.as_view(),
        name="inventory-detail",
    ),

    path(
        "variants/<uuid:variant_id>/inventory/stock-in/",
        StockInAPIView.as_view(),
        name="inventory-stock-in",
    ),

    path(
        "variants/<uuid:variant_id>/inventory/transactions/",
        InventoryTransactionAPIView.as_view(),
        name="inventory-transactions",
    ),
]