import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    )
    email = models.EmailField(unique=True)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='doctor')
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    

