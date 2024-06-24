from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializer import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import LeaderBoard
import jwt

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print("request: ", request.data)
        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
            leaderboard_entry = LeaderBoard(user_id =user, partidas_jugadas = 0)
            leaderboard_entry.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'video_url': 'skibidi authed'}
        return Response(content)

#Podemos implementar cualquiera de las dos pero yo preferiria usar IncreaseLeaderBoard
class UpdateLeaderBoard(APIView):
    authentication_classes = [JWTAuthentication]

    def patch(self, request, pk):
        jwt_value = request.headers.get('Authorization', '').split()[1]
        decoded_token = jwt.decode(jwt_value, options={'verify_signature': False})

        if decoded_token['is_superuser']:

            try:
                leaderboard_entry = LeaderBoard.objects.get(pk=pk)
            except LeaderBoard.DoesNotExist:
                return Response("Leaderboard with pk: ",pk, "DOESNT EXIST", status=status.HTTP_400_BAD_REQUEST)
            
            leaderboard_entry.partidas_jugadas = request.data['partidas_jugadas']
            leaderboard_entry.save()
            return Response("Entry saved!!!")
        return Response("You ARE NOT THE SUPER USER!")   

class IncreaseLeaderBoard(APIView):
    def patch(self, request, pk):
        jwt_value = request.headers.get('Authorization', '').split()[1]
        decoded_token = jwt.decode(jwt_value, options={'verify_signature': False})

        if decoded_token['is_superuser']:
            try:
                leaderboard_entry = LeaderBoard.objects.get(pk=pk)
            except LeaderBoard.DoesNotExist:
                return Response("Leaderboard with pk: ",pk, "DOESNT EXIST", status=status.HTTP_400_BAD_REQUEST)
            
            leaderboard_entry.partidas_jugadas += 1
            leaderboard_entry.save()
            return Response("Entry Saved !")
        return Response("You ARE NOT THE SUPER USER!")
