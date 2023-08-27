from django.db import models
from django.contrib.auth.models import AbstractUser


# Extends User's class
class User(AbstractUser):
    ident_number = models.CharField(max_length=50, verbose_name="Número de Identificación", unique=True)
