from apps.inventory.models import Inventory


class InventorySelector:
    @staticmethod
    def get_by_id(inventory_id):

        return (
            Inventory.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .get(
                id=inventory_id
            )
        )
    @staticmethod
    def get_by_variant(variant_id):

        return (
            Inventory.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .get(
                variant_id=variant_id
            )
        )
        
        
    @staticmethod
    def get_low_stock(
        threshold=10
    ):

        return (
            Inventory.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .filter(
                available_quantity__lte=threshold
            )
        )
        
    @staticmethod
    def get_out_of_stock():

        return (
            Inventory.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .filter(
                available_quantity=0
            )
        )
        
        
    @staticmethod
    def get_vendor_inventory(
        vendor_id
    ):

        return (
            Inventory.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .filter(
                variant__product__vendor_id=vendor_id
            )
        )
