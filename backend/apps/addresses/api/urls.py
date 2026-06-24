from django.urls import path

from .views import (
    AddressAPIView,
    AddressDetailAPIView,
)

urlpatterns = [

    path(
        "",
        AddressAPIView.as_view(),
        name="addresses",
    ),

    path(
        "<uuid:address_id>/",
        AddressDetailAPIView.as_view(),
        name="address-detail",
    ),
]