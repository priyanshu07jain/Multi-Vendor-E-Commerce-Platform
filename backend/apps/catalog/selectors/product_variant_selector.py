from apps.catalog.models import (
    ProductVariant
)


class ProductVariantSelector:

    @staticmethod
    def get_product_variants(
        product
    ):

        return (
            ProductVariant.objects
            .filter(
                product=product,
                is_active=True
            )
            .select_related(
                "product"
            )
        )
    
    @staticmethod
    def get_by_id(
        variant_id
    ):
        return ProductVariant.objects.get(
            id=variant_id,
            is_active=True,
        )