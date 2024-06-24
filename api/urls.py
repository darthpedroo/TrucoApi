from django.urls import path
from .views import Home, Register, UpdateLeaderBoard,IncreaseLeaderBoard


urlpatterns = [
    path('', Home.as_view()),
    path('register', Register.as_view()),
    path('leaderboard/<int:pk>', UpdateLeaderBoard.as_view()),
    path('increaseleaderboard/<int:pk>', IncreaseLeaderBoard.as_view()),
]