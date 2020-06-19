from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models


class User(AbstractUser):
    is_membership = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)
