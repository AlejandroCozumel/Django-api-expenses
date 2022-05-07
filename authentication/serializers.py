from ast import Try
import pdb
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.RegexField(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,20}$', error_messages={'invalid': 'Password must contain at least one lowercase letter, one uppercase letter, one number and one special character, 6 to 20 characters.'}, allow_blank=False, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)

    # Reset default message for password except invalid
    # def __init__(self, *args, **kwargs):
    #     super(RegisterSerializer, self).__init__(*args, **kwargs)
    #     self.fields['password'].error_messages['invalid'] = 'Password must contain at least one lowercase letter, one uppercase letter, one number and one special character'

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if User.objects.filter(email=email).first():
            raise serializers.ValidationError('Email has already been taken')
        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should be alphanumeric')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255, min_length=3, read_only=True)
    username = serializers.CharField(max_length=68, min_length=6)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # This allow us tho change token response, by default it looks to get_tokens.
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'tokens']

    def get_tokens(self, obj):  # By default it coneccts to SerializerMethodField
        user = User.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username, password=password)

        # import pdb
        # pdb.set_trace()

        if not user:
            raise AuthenticationFailed(
                'Invalid credentials, check email, password, and try again')

        if not user.is_verified:
            raise AuthenticationFailed('User is not verified')

        if not user.is_active:
            raise AuthenticationFailed('User is blocked, contact admin')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class ResetPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uid64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uid64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uid64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    'The reset password link is invalid or has expired', 401)

            user.set_password(password)
            user.save()

        except Exception as e:
            raise AuthenticationFailed(
                'The reset password link is invalid or has expired', 401)
        return super().validate(attrs)
