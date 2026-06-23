
from django.http import Http404
from apps.vendors.models import (
    Vendor,
    VendorMembership,
)


class VendorSelector:


    @staticmethod
    def get_user_vendors(user):

        return (
            Vendor.objects
            .filter(
                members__user=user
            )
            .distinct()
        )
        
    @staticmethod
    def get_user_vendor_by_id(
    user,
    vendor_id
    ):
     return Vendor.objects.get(
        id=vendor_id,
        members__user=user,
     )
     
    @staticmethod
    def get_user_membership(
    user,
    vendor
):
     return VendorMembership.objects.get(
        user=user,
        vendor=vendor,
    )

    @staticmethod
    def get_vendor_members(
    vendor
):
     return (
        VendorMembership.objects
        .filter(
            vendor=vendor
        )
        .select_related(
            "user"
        )
    )
     
     
    @staticmethod
    def get_vendor_membership(
    vendor,
    membership_id
):
     return VendorMembership.objects.get(
        id=membership_id,
        vendor=vendor,
    )