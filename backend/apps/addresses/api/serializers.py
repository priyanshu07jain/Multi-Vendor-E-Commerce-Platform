from rest_framework import serializers

from apps.addresses.models import (
    Address,
)


class AddressSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Address

        fields = "__all__"


class AddressCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Address

        exclude = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


class AddressUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Address

        exclude = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]