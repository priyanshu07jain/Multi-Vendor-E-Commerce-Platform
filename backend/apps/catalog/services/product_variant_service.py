from django.db import transaction

from apps.catalog.models import ProductVariant

from apps.vendors.models import (
    VendorMembership,
    MembershipRole,
)


class ProductVariantService:

    @staticmethod
    @transaction.atomic
    def create_variant(
        *,
        actor,
        product,
        name,
        sku,
        price,
    ):

        membership = (
            VendorMembership.objects.get(
                user=actor,
                vendor=product.vendor,
            )
        )

        if membership.role not in [
            MembershipRole.OWNER,
            MembershipRole.MANAGER,
        ]:
            raise ValueError(
                "Insufficient permissions."
            )

        return ProductVariant.objects.create(
            product=product,
            name=name,
            sku=sku,
            price=price,
        )