from apps.orders.models import (
    Order,
)


class OrderSelector:

    @staticmethod
    def get_user_orders(
        user
    ):

        return (
            Order.objects
            .filter(
                user=user
            )
            .select_related(
                "vendor"
            )
            .prefetch_related(
                "items"
            )
            .order_by(
                "-created_at"
            )
        )
    

    @staticmethod
    def get_order_by_id(
        *,
        user,
        order_id,
    ):

        return (
            Order.objects
            .select_related(
                "vendor"
            )
            .prefetch_related(
                "items",
                "items__variant",
            )
            .get(
                id=order_id,
                user=user,
            )
        )
    

    @staticmethod
    def get_vendor_orders(
    *,
    vendor_id,
):

        return (
        Order.objects
        .filter(
            vendor_id=vendor_id
        )
        .select_related(
            "user",
            "vendor",
        )
        .prefetch_related(
            "items"
        )
        .order_by(
            "-created_at"
        )
    )