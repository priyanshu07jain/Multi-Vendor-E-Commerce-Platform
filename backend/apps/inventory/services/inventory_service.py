from django.db import transaction
from django.core.exceptions import ValidationError

from apps.inventory.models import (
    Inventory,
    InventoryTransaction,
    TransactionType,
)


class InventoryService:

    @staticmethod
    def _create_transaction(
        inventory,
        transaction_type,
        quantity_delta,
        note="",
        reference_id=None,
    ):
        return InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type=transaction_type,
            quantity_delta=quantity_delta,
            note=note,
            reference_id=reference_id,
        )
        
        
    @staticmethod
    @transaction.atomic
    def add_stock(
        inventory_id,
        quantity,
        note="",
        reference_id=None,
    ):

        inventory = (
            Inventory.objects
            .select_for_update()
            .get(id=inventory_id)
        )

        inventory.available_quantity += quantity

        inventory.save(
            update_fields=[
                "available_quantity",
                "updated_at",
            ]
        )

        InventoryService._create_transaction(
            inventory=inventory,
            transaction_type=TransactionType.PURCHASE,
            quantity_delta=quantity,
            note=note,
            reference_id=reference_id,
        )

        return inventory
    
    
    
    @staticmethod
    @transaction.atomic
    def reserve_stock(
        inventory_id,
        quantity,
        note="",
        reference_id=None,
    ):

        inventory = (
            Inventory.objects
            .select_for_update()
            .get(id=inventory_id)
        )

        if inventory.available_quantity < quantity:
            raise ValidationError(
                "Insufficient stock."
            )

        inventory.available_quantity -= quantity
        inventory.reserved_quantity += quantity

        inventory.save(
            update_fields=[
                "available_quantity",
                "reserved_quantity",
                "updated_at",
            ]
        )

        InventoryService._create_transaction(
            inventory=inventory,
            transaction_type=TransactionType.RESERVE,
            quantity_delta=-quantity,
            note=note,
            reference_id=reference_id,
        )

        return inventory
    
    
    
    
    @staticmethod
    @transaction.atomic
    def release_stock(
        inventory_id,
        quantity,
        note="",
        reference_id=None,
    ):

        inventory = (
            Inventory.objects
            .select_for_update()
            .get(id=inventory_id)
        )

        if inventory.reserved_quantity < quantity:
            raise ValidationError(
                "Invalid release quantity."
            )

        inventory.available_quantity += quantity
        inventory.reserved_quantity -= quantity

        inventory.save(
            update_fields=[
                "available_quantity",
                "reserved_quantity",
                "updated_at",
            ]
        )

        InventoryService._create_transaction(
            inventory=inventory,
            transaction_type=TransactionType.RELEASE,
            quantity_delta=quantity,
            note=note,
            reference_id=reference_id,
        )

        return inventory
    
    
    
    
    @staticmethod
    @transaction.atomic
    def sell_stock(
        inventory_id,
        quantity,
        note="",
        reference_id=None,
    ):

        inventory = (
            Inventory.objects
            .select_for_update()
            .get(id=inventory_id)
        )

        if inventory.reserved_quantity < quantity:
            raise ValidationError(
                "Invalid sale quantity."
            )

        inventory.reserved_quantity -= quantity

        inventory.save(
            update_fields=[
                "reserved_quantity",
                "updated_at",
            ]
        )

        InventoryService._create_transaction(
            inventory=inventory,
            transaction_type=TransactionType.SALE,
            quantity_delta=-quantity,
            note=note,
            reference_id=reference_id,
        )

        return inventory
    
    
    
    
    
    
    @staticmethod
    @transaction.atomic
    def adjust_stock(
        inventory_id,
        quantity_delta,
        note="",
        reference_id=None,
    ):

        inventory = (
            Inventory.objects
            .select_for_update()
            .get(id=inventory_id)
        )

        new_quantity = (
            inventory.available_quantity
            + quantity_delta
        )

        if new_quantity < 0:
            raise ValidationError(
                "Inventory cannot be negative."
            )

        inventory.available_quantity = new_quantity

        inventory.save(
            update_fields=[
                "available_quantity",
                "updated_at",
            ]
        )

        InventoryService._create_transaction(
            inventory=inventory,
            transaction_type=TransactionType.ADJUSTMENT,
            quantity_delta=quantity_delta,
            note=note,
            reference_id=reference_id,
        )

        return inventory