from rest_framework import serializers

from apps.inventory.models import (
    Inventory,
    InventoryTransaction,
)


class StockInSerializer(
    serializers.Serializer
):

    quantity = serializers.IntegerField(
        min_value=1
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True
    )


class InventorySerializer(
    serializers.ModelSerializer
):

    variant_name = serializers.CharField(
        source="variant.name",
        read_only=True
    )

    class Meta:

        model = Inventory

        fields = [
            "id",
            "variant",
            "variant_name",
            "available_quantity",
            "reserved_quantity",
        ]


class InventoryTransactionSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = InventoryTransaction

        fields = [
            "id",
            "transaction_type",
            "quantity_delta",
            "note",
            "reference_id",
            "created_at",
        ]