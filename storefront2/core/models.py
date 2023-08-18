from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.\
# Inherit from AbstractUser to extend the User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
