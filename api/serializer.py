from rest_framework import serializers
from django.contrib.auth.models import User
from .models import LeaderBoard

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_superuser']

class LeaderBoardSerializer(serializers.ModelSerializer):
    class Meta: 
        model = LeaderBoard
        fields = ['user_id', 'partidas_jugadas']

