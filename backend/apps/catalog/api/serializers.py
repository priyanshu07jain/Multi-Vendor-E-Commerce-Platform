from rest_framework import serializers

from apps.catalog.models import Category
from apps.catalog.models import Product

class CategoryCreateSerializer(
    serializers.Serializer
):

    name = serializers.CharField(
        max_length=255
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    parent_id = serializers.UUIDField(
        required=False
    )

class CategorySerializer(
    serializers.ModelSerializer
):

    parent_name = serializers.CharField(
        source="parent.name",
        read_only=True
    )

    class Meta:

        model = Category

        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "parent_name",
            "is_active",
        ]



class ProductCreateSerializer(
    serializers.Serializer
):

    category_id = serializers.UUIDField()

    name = serializers.CharField(
        max_length=255
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

class ProductSerializer(
    serializers.ModelSerializer
):

    vendor_name = serializers.CharField(
        source="vendor.name",
        read_only=True
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:

        model = Product

        fields = [
            "id",
            "name",
            "slug",
            "description",
            "vendor",
            "vendor_name",
            "category",
            "category_name",
            "is_active",
        ]
        


class ProductVariantCreateSerializer(
    serializers.Serializer
):

    name = serializers.CharField(
        max_length=255
    )

    sku = serializers.CharField(
        max_length=100
    )

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )


from apps.catalog.models import (
    ProductVariant
)

class ProductVariantSerializer(
    serializers.ModelSerializer
):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:

        model = ProductVariant

        fields = [
            "id",
            "product",
            "product_name",
            "name",
            "sku",
            "price",
            "is_active",
        ]