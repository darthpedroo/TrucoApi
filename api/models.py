from django.db import models
from django.contrib.auth.models import User

class LeaderBoard(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    partidas_jugadas = models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()
    

# Create your models here.

