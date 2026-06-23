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