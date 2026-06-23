from django.db import transaction

from apps.cart.models import (
    CartItem,
)


class CartService:
    @staticmethod
    @transaction.atomic
    def add_item(
        *,
        cart,
        variant,
        quantity,
    ):

        item = (
            CartItem.objects.filter(
                cart=cart,
                variant=variant,
            )
            .first()
        )

        if item:

            item.quantity += quantity

            item.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

            return item

        return CartItem.objects.create(
            cart=cart,
            variant=variant,
            quantity=quantity,
        )
    @staticmethod
    @transaction.atomic
    def update_quantity(
        *,
        item,
        quantity,
    ):

        item.quantity = quantity

        item.save(
            update_fields=[
                "quantity",
                "updated_at",
            ]
        )

        return item
    @staticmethod
    @transaction.atomic
    def remove_item(
        *,
        item,
    ):

        item.delete()