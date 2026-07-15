from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data.get("username")
    password = serializer.validated_data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None and user.is_staff:
        return Response({
            "success": True,
            "message": "Login Successful"
        })

    return Response({
        "success": False,
        "message": "Invalid username or password"
    }, status=status.HTTP_401_UNAUTHORIZED)