from django.urls import path
from app.apis import *

urlpatterns = [
    path('register/', UserCreateAPI.as_view()),
    path('login/', UserLoginAPI.as_view()),
    path('user/', UserListAPI.as_view()),
]
