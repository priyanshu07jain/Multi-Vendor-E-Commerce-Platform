from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,UserSerializer
)

from rest_framework.permissions import (
    IsAuthenticated
)

class RegisterAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )
        
        
class MeAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )