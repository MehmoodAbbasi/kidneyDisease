from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='patient'):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password, role='admin')
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user