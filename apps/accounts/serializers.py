from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .utils import generate_code
from base.tasks import send_email


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        code = str(generate_code())
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            code=make_password(code),
        )
        send_email.delay("Account Verification", [user.email], "verify.html", {"first_name": user.first_name, "code": code})
        return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


# Verify serializer
class VerifySerializer(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.CharField()


# Send code serializer
class SendCodeSerializer(serializers.Serializer):
    email = serializers.CharField()


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
