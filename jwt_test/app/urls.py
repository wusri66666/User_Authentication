from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from app.apis import *

urlpatterns = [
    path('register/', UserCreateAPI.as_view()),
    path('login/', UserLoginAPI.as_view()),
    path('user/', UserListAPI.as_view()),

    # jwt的认证接口
    # 1、签发token
    path('obtain/', obtain_jwt_token),
    # 2、校验token
    path('verify/', verify_jwt_token),
    # 3、刷新token
    path('refresh/', refresh_jwt_token),
]
