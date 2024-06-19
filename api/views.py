from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializer import *

class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print("request: ", request.data)
        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )

            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'video_url': 'skibidi authed'}
        return Response(content)
