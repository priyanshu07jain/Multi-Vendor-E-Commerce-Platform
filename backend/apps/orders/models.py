from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User
from apps.vendors.models import Vendor
from apps.catalog.models import ProductVariant


class OrderStatus(
    models.TextChoices
):

    PENDING = "PENDING", "Pending"

    CONFIRMED = "CONFIRMED", "Confirmed"

    PAID = "PAID", "Paid"

    SHIPPED = "SHIPPED", "Shipped"

    DELIVERED = "DELIVERED", "Delivered"

    CANCELLED = "CANCELLED", "Cancelled"


class Order(BaseModel):

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    status = models.CharField(
        max_length=30,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:

        db_table = "orders"

        indexes = [
            models.Index(
                fields=["status"]
            ),
            models.Index(
                fields=["created_at"]
            )
        ]

    def __str__(self):

        return (
            f"Order {self.id}"
        )
    

class OrderItem(BaseModel):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT
    )

    product_name = models.CharField(
        max_length=255
    )

    variant_name = models.CharField(
        max_length=255
    )

    sku = models.CharField(
        max_length=100
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:

        db_table = "order_items"

    def __str__(self):

        return (
            f"{self.product_name}"
        )