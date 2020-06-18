from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models


class User(AbstractUser):
    is_membership = models.BooleanField(default=False)

