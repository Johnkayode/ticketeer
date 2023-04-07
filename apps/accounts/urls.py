from django.urls import path
from .views import RegisterApi, LoginApi, VerifyAccountAPI, SendCodeAPI, FetchUsersAPI, FetchUserAPI

urlpatterns = [
    path('register', RegisterApi.as_view()),
    path('login', LoginApi.as_view()),
    path('send-code', SendCodeAPI.as_view()),
    path('verify', VerifyAccountAPI.as_view()),
    path('', FetchUsersAPI.as_view()),
    path('<str:uid>', FetchUserAPI.as_view()),
]
