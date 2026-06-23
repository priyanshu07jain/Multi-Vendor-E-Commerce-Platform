from django.db import transaction
from django.utils.text import slugify

from apps.catalog.models import Product
from apps.vendors.models import (
    VendorMembership,
    MembershipRole,
)

class ProductService:

    @staticmethod
    @transaction.atomic
    def create_product(
        *,
        actor,
        vendor,
        category,
        name,
        description="",
    ):
        membership = (
            VendorMembership.objects.get(
                user=actor,
                vendor=vendor,
            )
        )

        if membership.role not in [
            MembershipRole.OWNER,
            MembershipRole.MANAGER,
        ]:

            raise ValueError(
                "Insufficient permissions."
            )
        product = Product.objects.create(
            vendor=vendor,
            category=category,
            name=name,
            slug=slugify(name),
            description=description,
        )

        return product