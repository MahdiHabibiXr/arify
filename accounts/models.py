from django.db import models
from django.contrib.auth.models import User


class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    charge = models.IntegerField()
    def __str__(self):
        return f'User {self.user.username} : Credits {self.charge}'
