from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, VerifySerializer, SendCodeSerializer
from .models import User
from .utils import generate_code
from base.tasks import send_email


# Register API
class RegisterApi(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })


# Login API
class LoginApi(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args,  **kwargs):
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email, password = serializer.data["email"], serializer.data["password"]
        user: User = User.objects.get(email=email)
        if not user:
            return Response(data={"message": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response(data={"message": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)
        user.id = user.uid
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "message": "Authentication successful.",
        })



# Verify account API
class VerifyAccountAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifySerializer

    def post(self, request, *args, **kwargs):
        serializer: VerifySerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email, code = serializer.data["email"], serializer.data["code"]
        user: User = User.objects.get(email=email)
        if not user:
            return Response(data={"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if not user.confirm_code(code=code):
            return Response(data={"message": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
        user.save()
        return Response({"message": "Account verification successful."})


# Verify account API
class SendCodeAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer: SendCodeSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user: User = User.objects.get(email=email)
        if not user:
            return Response(data={"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        code = str(generate_code())
        user.code = make_password(code)
        user.save()
        send_email.delay("Account Verification", [user.email], "verify.html", {"first_name": user.first_name, "code": code})
        print(code, user.code, check_password(code, user.code))
        return Response({"message": "Code sent."})


# Users API
class FetchUsersAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return Response({"users": UserSerializer(users, many=True, context=self.get_serializer_context()).data})