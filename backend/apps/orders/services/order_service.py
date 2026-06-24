from collections import defaultdict

from django.db import transaction
from django.core.exceptions import ValidationError

from apps.orders.models import (
    Order,
    OrderItem,
)

from apps.inventory.selectors.inventory_selector import (
    InventorySelector,
)

from apps.inventory.services.inventory_service import (
    InventoryService,
)


class OrderService:

    @staticmethod
    @transaction.atomic
    def checkout(
        *,
        cart,
    ):

        items = (
            cart.items
            .select_related(
                "variant",
                "variant__product",
                "variant__product__vendor",
            )
            .all()
        )

        if not items:
            raise ValidationError(
                "Cart is empty."
            )

        # Validate inventory first
        for item in items:

            inventory = (
                InventorySelector.get_by_variant(
                    item.variant.id
                )
            )

            if (
                inventory.available_quantity
                < item.quantity
            ):
                raise ValidationError(
                    f"Insufficient stock for "
                    f"{item.variant.name}"
                )

        # Group cart items by vendor
        vendor_items = defaultdict(list)

        for item in items:

            vendor = (
                item.variant
                .product
                .vendor
            )

            vendor_items[vendor].append(
                item
            )

        created_orders = []

        for vendor, vendor_cart_items in (
            vendor_items.items()
        ):

            order = Order.objects.create(
                user=cart.user,
                vendor=vendor,
            )

            order_total = 0

            for item in vendor_cart_items:

                variant = item.variant

                total_price = (
                    variant.price
                    * item.quantity
                )

                OrderItem.objects.create(
                    order=order,

                    variant=variant,

                    product_name=(
                        variant.product.name
                    ),

                    variant_name=(
                        variant.name
                    ),

                    sku=variant.sku,

                    quantity=item.quantity,

                    unit_price=variant.price,

                    total_price=total_price,
                )

                inventory = (
                    InventorySelector.get_by_variant(
                        variant.id
                    )
                )

                InventoryService.reserve_stock(
                    inventory_id=inventory.id,
                    quantity=item.quantity,
                    note="Checkout",
                    reference_id=order.id,
                )

                order_total += total_price

            order.total_amount = order_total

            order.save(
                update_fields=[
                    "total_amount",
                ]
            )

            created_orders.append(
                order
            )

        cart.items.all().delete()

        return created_orders