from django.db import transaction

from apps.addresses.models import (
    Address,
)


class AddressService:

    @staticmethod
    @transaction.atomic
    def create_address(
        *,
        user,
        **data,
    ):

        if data.get("is_default"):

            Address.objects.filter(
                user=user
            ).update(
                is_default=False
            )

        return Address.objects.create(
            user=user,
            **data,
        )

    @staticmethod
    @transaction.atomic
    def update_address(
        *,
        address,
        **data,
    ):

        if data.get("is_default"):

            Address.objects.filter(
                user=address.user
            ).exclude(
                id=address.id
            ).update(
                is_default=False
            )

        for field, value in data.items():

            setattr(
                address,
                field,
                value
            )

        address.save()

        return address

    @staticmethod
    @transaction.atomic
    def delete_address(
        *,
        address,
    ):

        address.delete()