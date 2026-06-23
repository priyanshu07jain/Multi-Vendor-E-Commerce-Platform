from django.db import models

from apps.catalog.models import ProductVariant
from apps.common.models import BaseModel

# Create your models here.
class Inventory(BaseModel):

    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory"
    )

    available_quantity = models.PositiveIntegerField(
        default=0
    )

    reserved_quantity = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        db_table = "inventories"
        

class TransactionType(models.TextChoices):

    PURCHASE = "PURCHASE", "Purchase"

    RESERVE = "RESERVE", "Reserve"

    RELEASE = "RELEASE", "Release"

    SALE = "SALE", "Sale"

    RETURN = "RETURN", "Return"

    DAMAGE = "DAMAGE", "Damage"

    ADJUSTMENT = "ADJUSTMENT", "Adjustment"
        
        
class InventoryTransaction(BaseModel):

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=TransactionType.choices
    )

    quantity_delta = models.IntegerField()

    note = models.TextField(
        blank=True
    )

    reference_id = models.UUIDField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = "inventory_transactions"

        indexes = [
            models.Index(
                fields=["transaction_type"]
            ),
            models.Index(
                fields=["created_at"]
            )
        ]