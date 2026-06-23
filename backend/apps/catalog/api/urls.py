from rest_framework import serializers

from apps.catalog.models import Category

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