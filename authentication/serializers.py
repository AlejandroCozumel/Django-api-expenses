import pdb
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.core.validators import RegexValidator

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    email=serializers.EmailField(max_length=255, min_length=3)

    class Meta:
      model=User
      fields=['email', 'username', 'password']

    def validate(self, attrs):
      email=attrs.get('email','')
      username=attrs.get('username','')

      if not username.isalnum():
        raise serializers.ValidationError('The username should be alphanumeric')
      return attrs

    def create(self, validated_data):
      return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.Serializer):
  token=serializers.CharField(max_length=555)

  class Meta:
    model=User
    fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
  email=serializers.EmailField(max_length=255, min_length=3, read_only=True)
  username=serializers.CharField(max_length=68, min_length=6)  
  password=serializers.CharField(max_length=68, min_length=6, write_only = True)
  tokens=serializers.CharField(max_length=68, min_length=6, read_only=True)

  class Meta:
    model=User
    fields=['email', 'username', 'password', 'tokens']

  def validate(self, attrs):
    username=attrs.get('username','')
    password=attrs.get('password','')

    user=auth.authenticate(username=username, password=password)

    # import pdb
    # pdb.set_trace()
    
    if not user:
      raise AuthenticationFailed('Invalid credentials, check email, password, and try again')

    if not user.is_verified:
      raise AuthenticationFailed('User is not verified')

    if not user.is_active:
      raise AuthenticationFailed('User is blocked, contact admin')

    return {
      'email': user.email,
      'username': user.username,
      'tokens': user.tokens()
    }