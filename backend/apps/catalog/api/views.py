from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.catalog.models import Category
from apps.catalog.services.category_service import (
    CategoryService
)
from apps.catalog.selectors.category_selector import (
    CategorySelector
)

from .serializers import (
    CategoryCreateSerializer,
    CategorySerializer,
)
from apps.catalog.models import (
    Category,
)

from apps.vendors.models import (
    Vendor,
)

from apps.catalog.services.product_service import (
    ProductService,
)

from apps.catalog.selectors.product_selector import (
    ProductSelector,
)

from .serializers import (
    ProductCreateSerializer,
    ProductSerializer,
)
from apps.catalog.models import Category

from apps.catalog.services.product_service import (
    ProductService,
)

from apps.catalog.selectors.product_selector import (
    ProductSelector,
)

from apps.vendors.selectors.vendor_selector import (
    VendorSelector,
)

from .serializers import (
    ProductCreateSerializer,
    ProductSerializer,
)
from apps.catalog.selectors.product_variant_selector import (
    ProductVariantSelector,
)

from apps.catalog.services.product_variant_service import (
    ProductVariantService,
)

from apps.catalog.models import ProductVariant

from rest_framework.exceptions import (
    ValidationError,
)

class CategoryAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        serializer = (
            CategoryCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        parent = None

        parent_id = (
            serializer.validated_data.get(
                "parent_id"
            )
        )

        if parent_id:

            parent = Category.objects.get(
                id=parent_id
            )

        category = (
            CategoryService.create_category(
                name=serializer.validated_data["name"],
                description=serializer.validated_data.get(
                    "description",
                    ""
                ),
                parent=parent,
            )
        )

        return Response(
            CategorySerializer(
                category
            ).data,
            status=status.HTTP_201_CREATED,
        )
    
    def get(
        self,
        request
    ):

        categories = (
            CategorySelector.get_categories()
        )

        serializer = (
            CategorySerializer(
                categories,
                many=True
            )
        )

        return Response(
            serializer.data
        )








class ProductAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        vendor_id
    ):

        vendor = (
            VendorSelector.get_user_vendor_by_id(
                user=request.user,
                vendor_id=vendor_id,
            )
        )

        serializer = (
            ProductCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = (
            Category.objects.get(
                id=serializer.validated_data[
                    "category_id"
                ]
            )
        )

        try:

            product = (
                ProductService.create_product(
                    actor=request.user,
                    vendor=vendor,
                    category=category,
                    name=serializer.validated_data[
                        "name"
                    ],
                    description=serializer.validated_data.get(
                        "description",
                        ""
                    ),
                )
            )

        except ValueError as e:

            raise ValidationError(
                str(e)
            )

        return Response(
            ProductSerializer(
                product
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def get(
        self,
        request,
        vendor_id
    ):

        vendor = (
            VendorSelector.get_user_vendor_by_id(
                user=request.user,
                vendor_id=vendor_id,
            )
        )

        products = (
            ProductSelector.get_vendor_products(
                vendor
            )
        )

        serializer = (
            ProductSerializer(
                products,
                many=True
            )
        )

        return Response(
            serializer.data
        )
    

class ProductVariantAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        product_id
    ):

        product = (
            ProductSelector.get_product_by_id(
                product_id=product_id
            )
        )

        serializer = (
            ProductVariantCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            variant = (
                ProductVariantService.create_variant(
                    actor=request.user,
                    product=product,
                    **serializer.validated_data
                )
            )

        except ValueError as e:

            raise ValidationError(
                str(e)
            )

        return Response(
            ProductVariantSerializer(
                variant
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def get(
        self,
        request,
        product_id
    ):

        product = (
            ProductSelector.get_product_by_id(
                product_id=product_id
            )
        )

        variants = (
            ProductVariantSelector.get_product_variants(
                product
            )
        )

        serializer = (
            ProductVariantSerializer(
                variants,
                many=True
            )
        )

        return Response(
            serializer.data
        )