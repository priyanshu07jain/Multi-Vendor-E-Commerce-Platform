from django.urls import path

from .views import (
    VendorCreateAPIView,
    VendorListAPIView,
    VendorDetailAPIView,
    VendorMemberAPIView
)

urlpatterns = [
    path(
        "",
        VendorCreateAPIView.as_view(),
        name="vendor-create",
    ),

    path(
        "my-vendors/",
        VendorListAPIView.as_view(),
        name="vendor-list",
    ),

    path(
        "<uuid:vendor_id>/",
        VendorDetailAPIView.as_view(),
        name="vendor-detail",
    ),

    path(
        "<uuid:vendor_id>/members/",
        VendorMemberAPIView.as_view(),
        name="vendor-members",
    ),

    path(
        "<uuid:vendor_id>/members/<uuid:membership_id>/",
        VendorMemberAPIView.as_view(),
        name="vendor-member-detail",
    ),
]