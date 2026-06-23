from apps.catalog.models import Product


class ProductSelector:

    @staticmethod
    def get_vendor_products(
        vendor
    ):
        return (
            Product.objects
            .filter(
                vendor=vendor,
                is_active=True
            )
            .select_related(
                "vendor",
                "category",
            )
        )
    @staticmethod
    def get_product_by_id(
        *,
        product_id,
    ):

        return Product.objects.get(
            id=product_id,
            is_active=True,
        )