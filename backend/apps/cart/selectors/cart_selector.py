from apps.cart.models import (
    Cart,
    CartItem,
)


class CartSelector:

    @staticmethod
    def get_user_cart(
        user
    ):

        cart, _ = (
            Cart.objects.get_or_create(
                user=user
            )
        )

        return cart

    @staticmethod
    def get_cart_item(
        *,
        cart,
        item_id,
    ):

        return (
            CartItem.objects.get(
                id=item_id,
                cart=cart,
            )
        )