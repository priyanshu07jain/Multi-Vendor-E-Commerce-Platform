from apps.inventory.models import (
    InventoryTransaction
)


class InventoryTransactionSelector:
    
    @staticmethod
    def get_inventory_transactions(
        inventory_id
    ):

        return (
            InventoryTransaction.objects
            .filter(
                inventory_id=inventory_id
            )
            .order_by("-created_at")
        )
        
        
        
    @staticmethod
    def get_sales_transactions():

        return (
            InventoryTransaction.objects
            .filter(
                transaction_type="SALE"
            )
            .order_by("-created_at")
        )
        
    @staticmethod
    def get_by_type(
        transaction_type
    ):

        return (
            InventoryTransaction.objects
            .filter(
                transaction_type=transaction_type
            )
            .order_by("-created_at")
        )