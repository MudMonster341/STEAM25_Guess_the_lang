from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_played = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
