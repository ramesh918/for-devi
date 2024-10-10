# users/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from .models import User
from assignments.utils import generate_jwt
from django.contrib.auth.hashers import check_password

class RegisterView(generics.CreateAPIView):
    """
    Endpoint for user/admin registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = RegisterSerializer(user).data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    """
    Endpoint for user/admin login.
    """
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_jwt(user)
        return Response({"token": token}, status=status.HTTP_200_OK)