from django.db import models
from django.contrib.auth.models import AbstractUser


# Extends User's class
class User(AbstractUser):
    ident_number = models.TextField(max_length=50, blank=True)
