from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User
from apps.catalog.models import ProductVariant


class Cart(BaseModel):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    def __str__(self):
        return f"{self.user.username} Cart"


class CartItem(BaseModel):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "variant"],
                name="unique_cart_variant"
            )
        ]

    def __str__(self):
        return (
            f"{self.variant.name} "
            f"({self.quantity})"
        )