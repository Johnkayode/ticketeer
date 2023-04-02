from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .models import User
from rest_framework.permissions import AllowAny


# Register API
class RegisterApi(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        print("User", user.password)
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
        print(user.password, password)
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
