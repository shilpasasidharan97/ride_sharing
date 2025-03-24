import uuid

from apps.user.api.serializers import (
    UserLoginSerializer,
    UserProfileResponseSerializer,
    UserRegistrationSerializer,
)
from apps.utils.token_encoder import jwt_encode
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class RegistrationAPIView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    response_serializer_class = UserProfileResponseSerializer

    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save(username=str(uuid.uuid4()))

        tokens = jwt_encode(user)
        django_login(request, user)
        return Response(
            {
                "access": tokens["access_token"],
                "refresh": tokens["refresh_token"],
                **self.response_serializer_class(
                    instance=user, context={"request": request}
                ).data,
            },
            status=201,
        )


class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    response_serializer_class = UserProfileResponseSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                UserProfileResponseSerializer(
                    instance=request.user,
                    context={"request": request},
                ).data
            )
        return Response({"message": "Unauthenticated! Please Login"}, status=401)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = jwt_encode(user)
        django_login(request, user)
        return Response(
            {
                "access": tokens["access_token"],
                "refresh": tokens["refresh_token"],
                **UserProfileResponseSerializer(
                    instance=user, context={"request": request}
                ).data,
            },
            status=200,
        )


class LogoutAPIView(APIView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        django_logout(self.request)
        return Response(
            {
                "message": "Logged Out! Kindly ensure you removed the token from client end!"
            },
            status=200,
        )
