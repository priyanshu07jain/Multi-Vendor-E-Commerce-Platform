from apps.addresses.models import (
    Address,
)


class AddressSelector:

    @staticmethod
    def get_user_addresses(
        user
    ):

        return (
            Address.objects
            .filter(
                user=user
            )
            .order_by(
                "-is_default",
                "-created_at",
            )
        )

    @staticmethod
    def get_user_address(
        *,
        user,
        address_id,
    ):

        return (
            Address.objects.get(
                id=address_id,
                user=user,
            )
        )