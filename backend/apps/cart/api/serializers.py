from rest_framework import serializers

from apps.cart.models import (
    CartItem,
)


class CartItemCreateSerializer(
    serializers.Serializer
):

    variant_id = serializers.UUIDField()

    quantity = serializers.IntegerField(
        min_value=1
    )


class CartItemUpdateSerializer(
    serializers.Serializer
):

    quantity = serializers.IntegerField(
        min_value=1
    )



class CartItemSerializer(
    serializers.ModelSerializer
):

    variant_name = serializers.CharField(
        source="variant.name",
        read_only=True
    )

    class Meta:

        model = CartItem

        fields = [
            "id",
            "variant",
            "variant_name",
            "quantity",
        ]

