from rest_framework import serializers

from apps.orders.models import (
    Order,
    OrderItem,
)


class OrderItemSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = OrderItem

        fields = [
            "id",
            "product_name",
            "variant_name",
            "sku",
            "quantity",
            "unit_price",
            "total_price",
        ]



class OrderSerializer(
    serializers.ModelSerializer
):

    items = (
        OrderItemSerializer(
            many=True,
            read_only=True
        )
    )

    vendor_name = serializers.CharField(
        source="vendor.name",
        read_only=True
    )

    class Meta:

        model = Order

        fields = [
            "id",
            "vendor",
            "vendor_name",
            "status",
            "total_amount",
            "created_at",
            "items",
        ]



