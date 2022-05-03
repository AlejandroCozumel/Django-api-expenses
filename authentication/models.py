from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
# Create your models here.

class UserManager(BaseUserManager):
  def create_user(self, username, email, password=None):
    if not username:
      raise ValueError('Users must have an username')
    if not email:
      raise ValueError('Users must have an email address')
    
    user=self.model(username=username, email=self.normalize_email(email))
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, username, email, password=None):
    if not password:
      raise ValueError('Password should not be none')
    
    user=self.create_user(username, email, password)
    user.is_superuser=True
    user.is_staff=True
    user.save()
    return user

class User(AbstractBaseUser, PermissionsMixin):
  username=models.CharField(max_length=255, unique=True, db_index=True)
  email=models.EmailField(max_length=255, unique=True, db_index=True)
  is_verified=models.BooleanField(default=False)
  is_staff=models.BooleanField(default=False)
  is_active=models.BooleanField(default=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  USERNAME_FIELD='username'
  REQUIRED_FIELDS=['email']

  objects=UserManager()

  def __str__(self):
    return self.email

  def tokens(self):
    return ''