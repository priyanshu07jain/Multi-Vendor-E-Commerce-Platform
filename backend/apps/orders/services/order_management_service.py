from django.db import transaction
from django.core.exceptions import ValidationError

from apps.orders.models import (
    OrderStatus,
)

from apps.inventory.selectors.inventory_selector import (
    InventorySelector,
)

from apps.inventory.services.inventory_service import (
    InventoryService,
)


class OrderManagementService:

    VALID_TRANSITIONS = {

        OrderStatus.PENDING: [
            OrderStatus.CONFIRMED,
            OrderStatus.CANCELLED,
        ],

        OrderStatus.CONFIRMED: [
            OrderStatus.PAID,
            OrderStatus.CANCELLED,
        ],

        OrderStatus.PAID: [
            OrderStatus.SHIPPED,
        ],

        OrderStatus.SHIPPED: [
            OrderStatus.DELIVERED,
        ],
    }

    @staticmethod
    @transaction.atomic
    def update_status(
        *,
        order,
        status,
    ):

        allowed = (
            OrderManagementService
            .VALID_TRANSITIONS
            .get(
                order.status,
                []
            )
        )

        if status not in allowed:

            raise ValidationError(
                "Invalid status transition."
            )

        order.status = status

        order.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(
        *,
        order,
    ):

        if order.status not in [

            OrderStatus.PENDING,
            OrderStatus.CONFIRMED,

        ]:

            raise ValidationError(
                "Order cannot be cancelled."
            )

        for item in order.items.all():

            inventory = (
                InventorySelector.get_by_variant(
                    item.variant.id
                )
            )

            InventoryService.release_stock(
                inventory_id=inventory.id,
                quantity=item.quantity,
                note="Order Cancelled",
                reference_id=order.id,
            )

        order.status = (
            OrderStatus.CANCELLED
        )

        order.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return order